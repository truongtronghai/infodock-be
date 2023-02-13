from collections import defaultdict

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Post
from ..serializers import PostSerializer

# Custom permission: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
class ReadOnlyAllow(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class SearchPostApiView(APIView):
    permission_classes = [ReadOnlyAllow]

    def get(self, request, search_string=""):
        """
        Description: search posts
        method: GET
        endpoint: /blog/search/<string>/?page=<number>
        Note: if page is invalid, error code is HTTP_404_NOT_FOUND and result is {"detail":"Invalid page"}
        """
        data = defaultdict(dict)
        try:
            posts = (
                Post.objects.filter(title__icontains=search_string)
                | Post.objects.filter(content__icontains=search_string)
            ).order_by("-edited_date")
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(posts, request)
            data = {
                "count": len(posts),
                "next_page": paginator.get_next_link(),
                "previous_page": paginator.get_previous_link(),
                "results": PostSerializer(result_page, many=True).data,
            }
        except Post.DoesNotExist:
            data = {}

        return Response(data, status=status.HTTP_200_OK)
