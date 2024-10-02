from django.shortcuts import render, redirect
from django.views import generic as views

from .models import Story
from ..ai_tools.text_generator import Categories

from ..auth_mixins.mixins import OwnerOfStoryRequiredMixin, CanGenerateStoryMixin


class StoriesGettingStarted(CanGenerateStoryMixin, views.TemplateView):
    template_name = 'generate_stories/getting-started.html'


class StoriesGenerateQuestionaryView(CanGenerateStoryMixin, views.TemplateView):
    template_name = 'generate_stories/generate-story-questionary.html'

    # Fill out a form, with info about the kids interests, the form will not be held in any database
    # and all info that will be entered will be stored in the session, until the customer resets, or
    # enters new details for a new story. This is due to regeneration of the story, if the customer does not
    # like the result.

    def post(self, request, *args, **kwargs):
        # TODO: If this is invoked it means the JS script is not working, maybe they have some blocking software
        return redirect('index')


class StoriesGenerateCategoryView(CanGenerateStoryMixin, views.TemplateView):
    template_name = 'generate_stories/generate-story-categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_info'] = Categories.info()
        return context


class StoriesViewStoryView(OwnerOfStoryRequiredMixin, views.DetailView):
    template_name = 'generate_stories/view-story.html'

    def get_queryset(self):
        return Story.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['info'] = self.format_object_info_into_tuple(self.object.info)
        return context

    @staticmethod
    def format_object_info_into_tuple(info):

        """
        Formats the story info that comes in a dict in the format {'urls': ...., 'paragraphs': ...}
        into a list of tuples with each image assigned to its paragraph [('url1', 'paragraph1'), ('url2', 'paragraph2')]...
        """

        try:
            result = []
            for i in range(len(info['urls'])):
                result.append((info['urls'][i], info['paragraphs'][i]))
            return result
        except IndexError or KeyError:
            return ()


class StoriesSamplesView(views.TemplateView):
    template_name = 'generate_stories/sample-stories.html'
