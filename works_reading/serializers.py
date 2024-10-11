from rest_framework import serializers
from works_reading.models import Bookmark
from works_writing.models import Work, Chapter
from works_writing.serializers import WorkSerializer, ChapterSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    work = WorkSerializer(read_only=True)
    binded_chapter = ChapterSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = '__all__'
