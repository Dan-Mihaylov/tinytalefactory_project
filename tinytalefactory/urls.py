from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('allauth.urls')),
    path('fun/', include('Tinytalefactory.generate_stories.urls')),
    path('', include('Tinytalefactory.common.urls')),
]

