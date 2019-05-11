from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework.response import Response

from user.serializers import UserSerializer

User = get_user_model()


class Register(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            User.objects.create_user(
                serialized.init_data['email'],
                serialized.init_data['username'],
                serialized.init_data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
