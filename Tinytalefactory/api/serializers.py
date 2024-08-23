from rest_framework import serializers
from django.contrib.auth import get_user_model
from Tinytalefactory.generate_stories.models import Story


UserModel = get_user_model()


class StoriesForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoriesForCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'info', 'slug']


class UserForUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name']
