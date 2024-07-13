from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StoriesGettingStarted.as_view(), name='getting-started'),
    path('questions/', views.StoriesGenerateQuestionaryView.as_view(), name='generate-story-questionary'),
    path('generate/<str:from_questionary>/', views.StoryGenerateView.as_view(), name='generate-story'),
]
