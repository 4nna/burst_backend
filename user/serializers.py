from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class DetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'matchable', 'current_location']


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['matchable', 'current_location']
