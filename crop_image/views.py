from PIL import Image
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageSerializer
from django.conf import settings
from . import constants

# Create your views here.
class UploadImageApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.data is not None:
            # using Serializer to deserialize request data to image file
            serializer = ImageSerializer(data=request.data)
            if serializer.is_valid():
                # save serializer to make uploaded file to be stored in storage (e.g. local storage)
                # after saving, the serializer.data["file"] keep the path of file
                serializer.save()

                try:
                    filename = str(settings.BASE_DIR) + serializer.data["file"]
                    im = Image.open(filename)
                    # METHOD 1: use resize() method of Image class of PIL to resize image
                    # im.resize(
                    #     (constants.RESIZED_IMAGE_WIDTH, constants.RESIZED_IMAGE_HEIGHT)
                    # ).save(filename)

                    # METHOD 2: use thumbnail() method of PIL
                    # This method is better because it makes resized image keep ratio
                    im.thumbnail(
                        (constants.RESIZED_IMAGE_WIDTH, constants.RESIZED_IMAGE_HEIGHT)
                    )
                    # save to replace original file
                    im.save(filename)
                    return Response(
                        {"filename": im.filename, "size(w,h)": str(im.size)},
                        status=status.HTTP_200_OK,
                    )
                except OSError:
                    return Response(
                        {"error": "Cannot open image to process"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "No request data"}, status=status.HTTP_200_OK)
