from django.shortcuts import render
from django.views import generic as views


class StoriesGettingStarted(views.TemplateView):
    template_name = 'generate_stories/getting-started.html'


