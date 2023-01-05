from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Category, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]
        depth = 3

    # def validate(self, attrs):
    #     return attrs

    # def update(self, instance, validated_data):
    #     # instance is object accessing this method
    #     return instance


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostInCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["title", "excerpt", "edited_date", "fig", "category", "user"]
