from django.urls import path
from . import views


urlpatterns = [
    path('list-stories/', views.StoriesListApiView.as_view(), name='api-list-stories'),
    path('generate/<str:from_questionary>/', views.StoryGenerateApiView.as_view(), name='api-generate-story'),
]