from api import serializers
from api.models import Post
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(data, status=status.HTTP_201_CREATED)


# List of all users
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


# Details of a user
class UserDetails(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


# Get all the posts
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [JWTAuthentication]

    # set the owner field to the current user
    def perform_create(self, serializer):
        # Check if the user is authenticated before assigning the owner
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            # Handle anonymous user differently or set a placeholder user
            anonymous_user, created = User.objects.get_or_create(username='anonymous')
            serializer.save(owner=anonymous_user)


# Get details of a post
class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    authentication_classes = [JWTAuthentication]
