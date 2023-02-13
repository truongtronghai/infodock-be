from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Category
from ..serializers import PostInCategorySerializer


class ListPostApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug=None):
        """
        Description: get list of posts in specific category
        method: GET
        endpoint: /blog/posts/<category slug>/?page=<number>
        Note: if page is invalid, error code is HTTP_404_NOT_FOUND and result is {"detail":"Invalid page"}
        """
        if slug == None:
            return Response(
                {"message": "slug of category required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            posts = Category.objects.get(
                slug=slug
            ).post_set.all()  # query reverse foreign key relationship
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(posts, request)
            data = {
                "count": posts.count(),
                "next_page": paginator.get_next_link(),
                "previous_page": paginator.get_previous_link(),
                "current_page": request.GET.get(paginator.page_query_param),
                "results": PostInCategorySerializer(
                    result_page, many=True
                ).data,  # when result_page has only 1 record, it can warn "UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered object_list"
            }
            return Response(data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
