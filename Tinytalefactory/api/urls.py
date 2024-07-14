from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoriesGenerateApiView.as_view(), name='api-generate-story')
]