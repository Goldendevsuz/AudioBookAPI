from rest_framework import serializers

from apps.chapter.models import Chapter


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
