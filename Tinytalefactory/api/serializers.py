from rest_framework import serializers

from Tinytalefactory.generate_stories.models import Story


class StoriesForListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoriesForCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['title', 'info']

