from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StoriesGettingStarted.as_view(), name='getting-started'),
    path('generate/', views.StoriesGenerateQuestionaryView.as_view(), name='generate-story-questionary'),
]
