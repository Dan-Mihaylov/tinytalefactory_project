import math

from django.contrib import admin
from . import models


@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'user', 'title', 'is_public', 'created_at', 'updated_at']

    list_filter = ['user', 'created_at', 'updated_at', 'is_public']
    search_fields = ['title']


@admin.register(models.Token)
class TokensAdmin(admin.ModelAdmin):
    list_display = ['user', 'purchased_tokens', 'promotional_tokens']


@admin.register(models.Usage)
class UsageAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'created_at', 'total_tokens']
    list_filter = ['created_at', 'user']


@admin.register(models.VerifiedEmail)
class VerifiedEmailAdmin(admin.ModelAdmin):

    list_display = ['email', 'created_at']
