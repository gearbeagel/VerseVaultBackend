from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from works.models import Work, Chapter, Tag
from works.serializers import WorkSerializer, ChapterSerializer, TagSerializer

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        work = serializer.save(author=self.request.user)
        first_chapter = Chapter.objects.create(
            title='Chapter 1',
            position=1,
            work=work,
        )
        return work, first_chapter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        work, first_chapter = self.perform_create(serializer)
        chapter_edit_url = reverse('chapters-detail', kwargs={'pk': first_chapter.id}, request=request)
        print(chapter_edit_url)
        response_data = serializer.data
        response_data['chapter_edit_url'] = chapter_edit_url
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)



class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [AllowAny]

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
