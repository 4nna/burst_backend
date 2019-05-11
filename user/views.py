from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import status, generics, permissions, mixins
from rest_framework.response import Response

from user.serializers import RegisterUserSerializer, DetailUserSerializer, UpdateUserSerializer

User = get_user_model()


class Update(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """
    Update current status (Is user matchable, current location of user) of an user.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UpdateUserSerializer

    def post(self, request, *args, **kwargs):
        """
        This method can only be called when user is authenticated (That means
        the request has an a authorization header in the request.

        Update status and current location of user
        """
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        serialized = UpdateUserSerializer(request.data)
        if serialized.is_valid():
            serialized.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class Detail(mixins.RetrieveModelMixin, generics.ListAPIView):
    """
    Get user's detail after logging in
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DetailUserSerializer

    def get(self, request, *args, **kwargs):
        """
        This method can only be called when user is authenticated (That means
        the request has an a authorization header in the request.

        Return detail of every user
        """
        if not request.user.is_authenticated:
            return HttpResponse(status=400)
        id = request.GET.get('id', None)
        if id is not None:
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)


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
            User.objects.create_user(
                serialized.init_data['email'],
                serialized.init_data['username'],
                serialized.init_data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
