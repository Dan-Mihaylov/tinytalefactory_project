from django.shortcuts import render, redirect
from django.views import generic as views

from .helpers import generate_story_from_questionary


class StoriesGettingStarted(views.TemplateView):
    template_name = 'generate_stories/getting-started.html'


class StoriesGenerateQuestionaryView(views.TemplateView):
    template_name = 'generate_stories/generate-story-questionary.html'

    # Fill out a form, with info about the kids interests, the form will not be held in any database
    # and all info that will be entered will be stored in the session, until the customer resets, or
    # enters new details for a new story. This is due to regeneration of the story, if the customer does not
    # like the result.

    def post(self, request, *args, **kwargs):
        # TODO: check the POST text validity
        self._add_story_info_to_session()
        return redirect('generate-story', from_questionary='true')

    def _add_story_info_to_session(self):

        story_info = {
            'name': self.request.POST.get('name', ''),
            'appearance': self.request.POST.get('appearance', ''),
            'story-about': self.request.POST.get('story-about', ''),
            'special-emphasis': self.request.POST.get('special-emphasis', '')
        }

        self.request.session['story_info'] = story_info


class StoryGenerateView(views.TemplateView):
    template_name = 'generate_stories/generate-story.html'
    story_text = ''  # need to split it by //n to receive a list of paragraphs
    tokens_used = 0
    images_urls = ['https://dm0qx8t0i9gc9.cloudfront.net/thumbnails/image/rDtN98Qoishumwih/cartoon-funny-teasing-face_Qk6e-G_thumb.jpg'] * 3

    def get(self, request, *args, **kwargs):
        if self._check_if_generate_from_questionary():
            story_info = self._extract_story_details_from_session()
            self.story_text, self.tokens_used = generate_story_from_questionary(
                story_info['name'],
                story_info['story-about'],
                story_info['special-emphasis'],
            )
            # TODO: generate story from questionary helper
            self._generate_images_for_each_paragraph()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tokens_used'] = self.tokens_used
        context['story_content'] = self._pack_paragraphs_and_img_urls_in_dict()
        return context

    def _pack_paragraphs_and_img_urls_in_dict(self):
        story_text = self.story_text.split('\\n')
        return {paragraph: img_url for paragraph, img_url in zip(story_text, self.images_urls)}

    def _check_if_generate_from_questionary(self):
        return self.kwargs.get('from_questionary', 'false') == 'true'

    def _extract_story_details_from_session(self):
        # {'name': ..., 'appearance': ..., 'story-about': ..., 'special-emphasis:...}
        return self.request.session['story_info']

    def _generate_images_for_each_paragraph(self):
        ...