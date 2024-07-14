from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from Tinytalefactory.api.serializers import StoriesForListSerializer, StoriesForCreateSerializer
from Tinytalefactory.generate_stories.models import Story


class StoriesGenerateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StoriesForListSerializer
        return StoriesForCreateSerializer

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)

    def get(self, request):
        stories = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer = serializer(stories, many=True)
        json = serializer.data
        return Response(json)

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        self.get(request)
