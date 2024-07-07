from django.contrib import admin
from . import models


# TODO: Change the display items
@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'user', 'title', 'created_at', 'updated_at']

    list_filter = ['user', 'created_at', 'updated_at']
    search_fields = ['title']


@admin.register(models.Token)
class TokensAdmin(admin.ModelAdmin):
    list_display = ['user', 'purchased_tokens', 'promotional_tokens']
