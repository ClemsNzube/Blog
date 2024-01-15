from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'posts']

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'owner']
