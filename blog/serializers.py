from dataclasses import fields

from pyexpat import model
from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]
        depth = 3

    # def validate(self, attrs):
    #     return attrs

    def update(self, instance, validated_data):
        """
        Because foreign related field is an object of Cateory, we need to override this method to process serializer's save()
        """
        try:
            fk_category = None
            if(validated_data.get("parent") is not None):
                fk_category = Category.objects.get(pk=validated_data.get("parent")["id"])
                
            instance.name = str(validated_data.get("name"))
            instance.slug = str(validated_data.get("slug"))
            instance.parent = fk_category
            instance.save()  # REMEMBER to save instance to update record of instance
        except Category.DoesNotExist:
            pass

        return instance
