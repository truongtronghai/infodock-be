from collections import defaultdict

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    BasePermission,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (
    ViewSet,
)  # https://testdriven.io/blog/drf-views-part-3/

from .models import Category, Post
from .serializers import CategorySerializer, PostInCategorySerializer, PostSerializer

# Create your views here.

# Custom permission: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
class ReadOnlyAllow(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class CategoryViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    def list(self, request):
        """
        method: GET
        endpoint: /blog/category/
        """
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        method: GET
        endpoint: /blog/category/<pk>/
        """
        try:
            item = self.queryset.get(pk=pk)
            serializer = CategorySerializer(item)
            return Response(
                {"message": "Category existed", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Category.DoesNotExist:
            return Response(
                {"message": "No category found"}, status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        method: POST
        endpoint: /blog/category/
        Parameters:
            JSON data: {
                "name":<category>,
                "slug":<slug of category name>,
                "parent": <id>
                }
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # get the parent category to append to validated_data
            if request.data.get("parent") is None:
                serializer.validated_data["parent"] = None
            else:
                try:
                    serializer.validated_data["parent"] = Category.objects.get(
                        pk=request.data.get("parent")
                    )
                except Category.DoesNotExist:
                    return Response(
                        {"message": "Parent ID is not existed"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            # print(serializer.validated_data)
            serializer.save()
            return Response({"message": "Category created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        method: PUT
        endpoint: /blog/category/<pk>/
        Parameters:
            id : passing as querystring
            JSON data: {
                "name":<category>,
                "slug":<slug of category name>,
                "parent": <id>
                }
        """
        if pk is None:
            return Response(
                {"message": "No category ID for updating"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                category = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                return Response(
                    {"message": "No category found for updating"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # having object passed means updating
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            # get the parent category to append to validated_data
            if request.data.get("parent") is None:
                serializer.validated_data["parent"] = None
            else:
                try:
                    serializer.validated_data["parent"] = Category.objects.get(
                        pk=request.data.get("parent")
                    )
                except Category.DoesNotExist:
                    return Response(
                        {"message": "Parent ID is not existed"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

            serializer.save()
            return Response(
                {"message": "Category updated", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        method: DELETE
        endpoint: /blog/category/<pk>/
        Parameters:
            id : passing as querystring
        """
        if pk is None:
            return Response(
                {"message": "ID of category is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif int(pk) == 1:
            return Response(
                {"message": "Deleting default category is not allowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Category.objects.get(pk=pk).delete()
            return Response(
                {"message": "Category deleted successfully"}, status=status.HTTP_200_OK
            )
        except Category.DoesNotExist:
            return Response(
                {"message": "Category does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


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
                "count": len(posts),
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
