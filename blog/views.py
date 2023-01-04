from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (
    ViewSet,
)  # https://testdriven.io/blog/drf-views-part-3/

from .models import Category
from .serializers import CategorySerializer


# Create your views here.
class CategoryViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
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
            print(serializer.validated_data)
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


class PostApiView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)
    