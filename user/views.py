from collections import deque

from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions, mixins
from rest_framework.response import Response

from location.models import Location
from user.serializers import RegisterUserSerializer, DetailUserSerializer, UpdateUserSerializer

User = get_user_model()
available_users = deque()


class Update(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    Update current status (Is user matchable, current location of user) of an user.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UpdateUserSerializer

    def post(self, request, *args, **kwargs):
        """
        Update status and current location of user. Authentication required.
        """
        if not request.user.is_authenticated:
            return Response("You have to log yourself in", status=403)
        serialized = UpdateUserSerializer(data=request.data)
        if serialized.is_valid():
            user = request.user
            user.matchable = serialized['matchable']
            user.current_location = Location(serialized['current_location'])
            user.save()
            if len(available_users) > 0:
                candidate = deque.pop(available_users)
            else:
                return Response("There are currently no user around", status=200)
        return Response("An error has happened, please try again!", status=400)


class Detail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Get user's detail after logging in
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DetailUserSerializer

    def get(self, request, *args, **kwargs):
        """
        Return detail of every user. Authentication required.
        """
        if not request.user.is_authenticated:
            return Response("Please authenticate yourself", status=403)
        else:
            user = self.queryset.get(username=request.user)
            serialized = DetailUserSerializer(user)
            return Response(data=serialized.data, status=200)


class Register(generics.CreateAPIView):
    """
    Register a new user
    """
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Create a new user with email, username, password
        """
        serialized = RegisterUserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create_user(
                email=serialized.data['email'],
                username=serialized.data['username'],
                password=serialized.data['password']
            )
            user.save()
            return Response("User created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
