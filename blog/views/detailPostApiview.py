from rest_framework.permissions import (
    AllowAny,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Post
from ..serializers import PostSerializer
from rest_framework import status


class DetailPostApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug=None):
        """
        Description: get single post with slug
        method: GET
        endpoint: /blog/<slug>
        """
        try:
            post = Post.objects.get(slug=slug)
            return Response(
                {"data": PostSerializer(post).data}, status=status.HTTP_200_OK
            )
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
