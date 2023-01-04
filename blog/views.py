from collections import OrderedDict
from datetime import datetime
from unicodedata import category

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import \
    ViewSet  # https://testdriven.io/blog/drf-views-part-3/

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
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category created"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):  # http method = PUT
        """
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

        serializer = CategorySerializer(
            category, data=request.data
        )  # having object passed means updating

        if serializer.is_valid():
            # get the parent category to append to validated_data
            try:
                serializer.validated_data["parent"] = CategorySerializer(
                    Category.objects.get(pk=request.data.get("parent"))
                ).data  # needs serialized data, so I used this line
            except Category.DoesNotExist:
                serializer.validated_data["parent"] = None

            serializer.save()  # overridden in CategorySerializer's update()
            return Response(
                {"message": "Category updated", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
