from django.contrib.auth.models import User
from rest_framework import serializers

from user_auth.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']

    def validate_username(self, value):
        if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'location', 'icon_name', 'user_type']
        required = ['user', 'user_type']