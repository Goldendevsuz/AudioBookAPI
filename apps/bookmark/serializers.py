from rest_framework import serializers

from .models import EbookBookmark, AudiobookBookmark


class EbookBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EbookBookmark
        fields = ['id', 'user', 'book', 'page']
        read_only_fields = ['user']


class AudiobookBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudiobookBookmark
        fields = ['id', 'user', 'book', 'chapter', 'position']
        read_only_fields = ['user']
