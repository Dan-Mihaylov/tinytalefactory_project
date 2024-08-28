from django.urls import path
from . import views


urlpatterns = [
    path('list-stories/', views.StoriesListApiView.as_view(), name='api-list-stories'),
    path('generate/<str:from_questionary>/', views.StoryGenerateApiView.as_view(), name='api-generate-story'),
    path('users/', views.UserInfoChangeApiView.as_view(), name='api-change-user-info'),
    path('story/<slug:slug>/', views.StoryRetrieveApiView.as_view(), name='api-retrieve-story'),
    path('samples/', views.StoriesListSampleApiView.as_view(), name='api-list-samples'),
    path('base-stats/', views.StoriesAndUsersCountApiView.as_view(), name='api-base-stats'),
]