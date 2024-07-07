from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.StoriesGettingStarted.as_view(), name='getting-started'),
]
