from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoriesListCreateApi.as_view(), name='api-list-create-stories'),
    path('generate/<str:from_questionary>/', views.StoryGenerateApi.as_view(), name='api-generate-story'),
]