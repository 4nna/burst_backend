from collections import deque

from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions, mixins
from rest_framework.response import Response

from user.serializers import RegisterUserSerializer, DetailUserSerializer, UpdateUserSerializer, SimpleUserSerializer
from location.models import distance, CENTER, RADIUS, Location

User = get_user_model()

available_users = deque()


class CountOnline(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UpdateUserSerializer
    """
    Number of users who are matchable in the meeting zone
    """

    def get(self, request, *args, **kwargs):
        """
        Number of users who are matchable in the meeting zone
        """
        return Response(f'Number of available users {len(available_users)}', status=200)


class Update(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    Update current status (Is user matchable, current location of user) of an user.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = SimpleUserSerializer

    def post(self, request, *args, **kwargs):
        """
        Update status and current location of user. Authentication required.
        """
        if not request.user.is_authenticated:
            return Response("You have to log yourself in", status=403)
        serialized = SimpleUserSerializer(data=request.data)
        if serialized.is_valid():
            user = request.user
            location_dict = serialized.data['current_location']
            matchable = serialized.data['matchable']
            user.matchable = matchable
            if not user.matchable:
                user.other_user.other_user = None
                user.other_user.save()
                user.other_user = None
                user.save()
                serialized = UpdateUserSerializer(user)
                return Response(serialized.data, status=200)
            location = Location(longtitude=location_dict['longtitude'], latitude=location_dict['latitude'])
            location.save()
            user.current_location = location
            user.save()
            if user.current_location is not None and distance(CENTER,
                                                              user.current_location) < RADIUS and user.matchable:
                if len(available_users) > 0:
                    candidate = available_users.pop()
                    user.other_user = candidate
                    candidate.other_user = user
                    user.matchable = False
                    candidate.matchable = False
                    candidate.save()
                    user.save()
                elif user.matchable:
                    available_users.append(user)
            serialized = UpdateUserSerializer(user)
            return Response(serialized.data, status=200)
        return Response("Invalid request", status=400)


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
            user.is_staff = True
            user.save()
            return Response("User created successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
