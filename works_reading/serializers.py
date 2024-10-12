from rest_framework import serializers
from works_reading.models import Bookmark
from works_writing.models import Work, Chapter
from works_writing.serializers import WorkSerializer, ChapterSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    work = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all())
    binded_chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all(), allow_null=True)

    class Meta:
        model = Bookmark
        fields = '__all__'
