from django.contrib.auth import get_user_model
from rest_framework import serializers

from location.serializers import LocationSerializer

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class DetailUserSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'matchable', 'current_location']


class UpdateUserSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(many=False, write_only=True)
    class Meta:
        model = User
        fields = ['matchable', 'current_location']
