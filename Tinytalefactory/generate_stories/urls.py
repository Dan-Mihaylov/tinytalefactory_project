from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StoriesGettingStarted.as_view(), name='getting-started'),
    path('questions/', views.StoriesGenerateQuestionaryView.as_view(), name='generate-story-questionary'),
    path('categories/', views.StoriesGenerateCategoryView.as_view(), name='generate-story-categories'),
    path('view/<slug:slug>/', views.StoriesViewStoryView.as_view(), name='view-story'),
]
