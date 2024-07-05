from django.contrib import admin
from . import models


# TODO: Change the display items
@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'user', 'title', 'info']


@admin.register(models.Token)
class TokensAdmin(admin.ModelAdmin):
    list_display = ['user', 'purchased_tokens', 'promotional_tokens']
