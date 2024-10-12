from rest_framework import serializers

from works_writing.models import Work, Chapter, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class WorkSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ChapterSerializer(serializers.ModelSerializer):
    work = serializers.PrimaryKeyRelatedField(
        queryset=Work.objects.all(),
        required=False
    )

    class Meta:
        model = Chapter
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'work')

    def create(self, validated_data):
        work_id = validated_data.pop('work_id', None)
        chapter = Chapter.objects.create(**validated_data, work_id=work_id)
        return chapter
