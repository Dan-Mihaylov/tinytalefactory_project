from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from Tinytalefactory.api.serializers import StoriesForListSerializer, StoriesForCreateSerializer
from Tinytalefactory.generate_stories.helpers import generate_story_from_questionary
from Tinytalefactory.generate_stories.models import Story, Usage


class StoriesListCreateApi(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StoriesForListSerializer

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)

    def get(self, request):
        stories = self.get_queryset()
        serializer = self.serializer_class(stories, many=True)
        json = serializer.data
        return Response(json)


class StoryGenerateApi(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = StoriesForCreateSerializer
    story_text = ''  # need to split it by | to receive a list of paragraphs
    story_title = ''
    tokens_used = 0
    images_urls = [
        'https://images.pexels.com/photos/6898860/pexels-photo-6898860.jpeg?auto=compress&cs=tinysrgb&w=800&h=460&dpr=1'
                  ] * 3

    def get(self, request, *args, **kwargs):

        json = ["Something went wrong"]  # Default response
        bad_response = json

        if self._check_if_generate_from_questionary():
            story_info = self._extract_story_details_from_get()
            self.story_text, self.tokens_used = generate_story_from_questionary(
                story_info['name'],
                story_info['story-about'],
                story_info['special-emphasis'],
            )

            self.story_text = self._split_paragraph()
            self.story_title = story_info['title'] if story_info['title'] != '' else f'The story of {story_info["name"]}'
            self._generate_images_for_each_paragraph()
            # TODO: When creating story from categories, take json out
            json = self._create_json_object()

        response = Response(json, status=status.HTTP_200_OK)
        if json == bad_response:
            return response
        else:
            self._submit_tokens_used_info()
            return self._create_story(json)

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

    def _generate_images_for_each_paragraph(self):
        ...

    def _create_json_object(self,):
        return {
            "title": "Title-1",
            "info": {
                "paragraphs": [p.strip() for p in self.story_text],
                "urls": self.images_urls
            }
        }

    def _split_paragraph(self):
        return self.story_text.split('|')

    def _create_story(self, data):
        serializer = self.serializer_class(data=data)
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
