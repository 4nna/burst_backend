from django.contrib.auth import get_user_model
from rest_framework import serializers

from location.serializers import LocationSerializer

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(many=False)

    class Meta:
        model = User
        fields = ['matchable', 'current_location', 'id', 'email']


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class DetailUserSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(many=False, read_only=True)
    other_user = SimpleUserSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'matchable', 'current_location', 'other_user']


class UpdateUserSerializer(serializers.ModelSerializer):
    current_location = LocationSerializer(many=False)
    other_user = SimpleUserSerializer(many=False)

    class Meta:
        model = User
        fields = ['matchable', 'current_location', 'other_user']
