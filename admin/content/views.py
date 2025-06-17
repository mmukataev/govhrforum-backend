import os

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Speaker, News, Registration
from .serializers import SpeakerSerializer, NewsSerializer, RegistrationSerializer
from django.core.files.base import ContentFile

class SpeakerListView(generics.ListAPIView):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer


class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        # Сначала сохраняем объект, чтобы получить id
        instance = serializer.save()

        if instance.photo:
            # Читаем содержимое файла
            photo_data = instance.photo.read()

            # Формируем новое имя файла
            new_filename = f'{instance.id}.jpg'

            # Перезаписываем фото новым именем
            instance.photo.save(new_filename, ContentFile(photo_data), save=True)
            