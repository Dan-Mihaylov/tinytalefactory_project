from rest_framework import serializers
from django.contrib.auth import get_user_model
from Tinytalefactory.generate_stories.models import Story
from Tinytalefactory.paypal.models import Order
from Tinytalefactory.common.models import Notification


UserModel = get_user_model()


class StoriesSamplesForListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ['title', 'info', 'slug']


class StoriesForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoriesForCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'info', 'slug']


class StoriesForRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Story
        fields = ['created_at', 'updated_at', 'title', 'info',]


class UserForUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name']


class OrderForCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['user', 'reference', 'quantity', 'price', 'status']


class NotificationForCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['user', 'content']


class NotificationForRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['pk', 'content', 'created_at', 'seen', '__str__']


class NotificationForUpdateSeenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['seen']
