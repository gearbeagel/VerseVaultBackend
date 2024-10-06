from django.contrib.auth.models import User
from rest_framework import serializers

from user_auth.models import Profile, WriterStats, ReaderStats, Favorite
from works_writing.serializers import WorkSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']

    def validate_username(self, value):
        if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

class WriterStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WriterStats
        fields = '__all__'

class ReaderStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReaderStats
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'icon_name', 'user_type']
        required = ['user', 'user_type']

class FavoriteSerializer(serializers.ModelSerializer):
    work = WorkSerializer()
    profile = ProfileSerializer()
    class Meta:
        model = Favorite
        fields = '__all__'