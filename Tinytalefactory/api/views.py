from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics as APIGenericView
from rest_framework.response import Response

from Tinytalefactory.api.serializers import (
    StoriesForListSerializer,
    StoriesForCreateSerializer,
    UserForUpdateSerializer
)
from Tinytalefactory.generate_stories.helpers import (
    generate_story_from_questionary,
    generate_images_from_paragraphs,
    generate_story_from_category
)
from Tinytalefactory.generate_stories.models import Story, Usage

from django.contrib.auth import get_user_model


UserModel = get_user_model()


class StoriesListApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoriesForListSerializer

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)

    def get(self, request):
        stories = self.get_queryset()
        serializer = self.serializer_class(stories, many=True)
        json = serializer.data
        return Response(json)


class StoryGenerateApiView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = StoriesForCreateSerializer
    story_text = []
    story_title = ''
    tokens_used = 0
    # images_urls = ['https://images.pexels.com/photos/4790613/pexels-photo-4790613.jpeg?auto=compress&cs=tinysrgb&w=250&h=250&dpr=1'] * 3
    images_urls = []

    def get(self, request, *args, **kwargs):

        json = ["Something went wrong"]  # Default response
        bad_response = json
        appearance = ''

        if self._check_if_generate_from_questionary():
            story_info = self._extract_story_details_from_get()
            appearance = story_info['appearance']
            self.story_text, self.tokens_used = generate_story_from_questionary(
                story_info['name'],
                story_info['story-about'],
                story_info['special-emphasis'],
            )

            self.story_title = story_info['title'] if story_info['title'] != '' else f'The story of {story_info["name"]}'
        else:
            story_category = self._extract_story_category()
            response_text_list, self.tokens_used = generate_story_from_category(story_category)
            self._get_story_paragraphs_and_title_from_generate_from_questionary(response_text_list)

        self._generate_images_for_each_paragraph(appearance)
        json = self._create_json_object()
        response = Response(json, status=status.HTTP_200_OK)

        if json == bad_response:
            return response
        else:
            self._submit_tokens_used_info()
            return self._create_story(json)

    def _extract_story_category(self):
        return self.request.GET.get('category', '')

    def _get_story_paragraphs_and_title_from_generate_from_questionary(self, response_text_list):
        self.story_text = response_text_list[1::]
        self.story_title = response_text_list[0]

    def _check_if_generate_from_questionary(self):
        return self.kwargs.get('from_questionary', 'false') == 'true'

    # def _extract_story_details_from_session(self):
    #     # {'name': ..., 'appearance': ..., 'story-about': ..., 'special-emphasis:...}
    #     return self.request.session['story_info']

    def _extract_story_details_from_get(self):

        # TODO: Format to extract_story_details which will call this one and if no result call extract from session

        story_info = {
            'name': self.request.GET.get('name', ''),
            'story-about': self.request.GET.get('story-about', ''),
            'special-emphasis': self.request.GET.get('special-emphasis', ''),
            'appearance': self.request.GET.get('appearance', ''),
            'title': self.request.GET.get('title', ''),
        }

        if any([story_info[key] != '' for key in story_info]):
            self._add_story_info_to_session(story_info)

        return story_info

    # TODO: When text is split into paragraphs, feed each paragraph into image generator, and generate the images.

    def _generate_images_for_each_paragraph(self, appearance=''):
        images = []
        for paragraph in self.story_text:
            images.append(generate_images_from_paragraphs(paragraph, appearance))
        self.images_urls = images
        return

    def _create_json_object(self,):
        return {
            "title": self.story_title,
            "info": {
                "paragraphs": self.story_text,
                "urls": self.images_urls
            }
        }

    def _create_story(self, data):
        serializer = self.serializer_class(data=data)
        # TODO: If valid - Take one token for story creation from user.
        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _submit_tokens_used_info(self):
        if self.tokens_used > 0:
            return Usage.objects.create(user=self.request.user, total_tokens=self.tokens_used)

    def _add_story_info_to_session(self, story_info: dict):

        """
        Add story info to the session in case customer does not like the result and wants to regenerate
        """
        self.request.session['story_info'] = story_info


class UserInfoChangeApiView(APIGenericView.RetrieveUpdateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserForUpdateSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

