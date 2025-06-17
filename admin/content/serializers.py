from rest_framework import serializers
from .models import Speaker, News, Registration

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['id', 'name_kz', 'name_ru', 'name_en', 'role', 'description_kz', 'description_ru', 'description_en', 'photo', 'priority']

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title_kz', 'title_ru', 'title_en', 'description_kz', 'description_ru', 'description_en', 'url_kz', 'url_ru', 'url_en', 'img']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ['id', 'name', 'surname', 'patronymic', 'organization', 'position', 'country', 'email', 'phone', 'session', 'consent', 'foresight_topics', 'iin', 'photo']