from django.contrib import admin
from django.urls import path, include

from Tinytalefactory.allauth.account import views as allauth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/signup/', allauth_views.signup, name='signup'),
    path('account/password/reset/', allauth_views.reset, name='reset'),
    path('account/', include('allauth.urls')),
    path('stories/', include('Tinytalefactory.generate_stories.urls')),
    path('api/', include('Tinytalefactory.api.urls')),
    path('profile/', include('Tinytalefactory.profile.urls')),
    path('', include('Tinytalefactory.common.urls')),
    path('', include('Tinytalefactory.paypal.urls')),
]

