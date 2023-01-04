from rest_framework import serializers

from .models import Category, Post


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
    class Meta:
        model = Post
        fields = "__all__"
