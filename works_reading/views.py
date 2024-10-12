from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from works_reading.models import Bookmark
from works_reading.serializers import BookmarkSerializer
from works_writing.models import Work, Chapter
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

    def create(self, request, *args, **kwargs):
        try:
            work = Work.objects.get(pk=request.data['work'])
        except Work.DoesNotExist:
            return Response({'error': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)

        binded_chapter = None
        if request.data.get('bm_type') == 'BM-C':
            try:
                binded_chapter = Chapter.objects.get(pk=request.data['binded_chapter'])
            except Chapter.DoesNotExist:
                return Response({'error': 'Chapter not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data={
            **request.data,
            'user': request.user.id,
            'work': work.id,
            'binded_chapter': binded_chapter.id if binded_chapter else None
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        bm_id = kwargs.get('pk')

        try:
            bm = Bookmark.objects.get(id=bm_id)
        except Bookmark.DoesNotExist:
            raise NotFound(detail="Favorite not found.")

        bm.delete()

        return Response({
            "detail": "Removed from bookmark. :c"
        }, status=status.HTTP_204_NO_CONTENT)