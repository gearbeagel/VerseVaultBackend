from rest_framework import serializers

from works.models import Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')