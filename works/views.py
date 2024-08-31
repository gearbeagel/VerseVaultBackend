from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from works.models import Work, Chapter
from works.serializers import WorkSerializer


# Create your views here.

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = WorkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        work = serializer.save()
        chapter = Chapter.objects.create(
            title='Chapter 1',
            position=1,
            work=work,
        )
        chapter.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

