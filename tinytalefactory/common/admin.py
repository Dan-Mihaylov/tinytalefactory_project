from django.contrib import admin
from . import models


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ['pk', 'user', 'seen', 'created_at', '__str__']
    list_filter = ['user', 'seen', 'created_at']
    search_fields = ['user']
