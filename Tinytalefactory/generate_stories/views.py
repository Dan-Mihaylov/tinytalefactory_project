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
        # TODO: If this is invoked it means the JS script is not working, maybe they have some blocking software
        return redirect('index')

