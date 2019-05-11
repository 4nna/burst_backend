import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import serializers
from django.http import HttpResponse
from rest_framework import status, generics, permissions, mixins
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework_jwt.serializers import jwt_payload_handler

import user
from user.serializers import RegisterUserSerializer, DetailUserSerializer

User = get_user_model()


class Detail(mixins.RetrieveModelMixin, generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetailUserSerializer

    def get(self, request, *args, **kwargs):
        id = request.GET.get('id', None)
        if id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


class Register(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serialized = RegisterUserSerializer(data=request.data)
        if serialized.is_valid():
            User.objects.create_user(
                serialized.init_data['email'],
                serialized.init_data['username'],
                serialized.init_data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
