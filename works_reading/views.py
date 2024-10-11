from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from works_reading.models import Bookmark
from works_reading.serializers import BookmarkSerializer
from works_writing.models import Work
from works_writing.serializers import WorkSerializer


# Create your views here.
class WorksReadingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Work.objects.filter(posted=True).order_by('-created_at')


class BookmarksViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.all().order_by('-created_at')
