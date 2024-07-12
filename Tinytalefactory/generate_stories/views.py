from django.shortcuts import render
from django.views import generic as views


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
        return render(request, self.template_name)

    def _add_story_info_to_session(self):

        story_info = {
            'name': self.request.POST.get('name', ''),
            'appearance': self.request.POST.get('appearance', ''),
            'story-about': self.request.POST.get('story-about', ''),
            'special-emphasis': self.request.POST.get('special-emphasis', '')
        }

        self.request.session['story_info'] = story_info
