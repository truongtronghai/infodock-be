from multiprocessing import managers

from django.db.models import Model
from rest_framework.renderers import JSONRenderer

from blog.models import Category
from blog.serializers import CategorySerializer

cates = Category.objects.get(pk=7).category_set.all()
seri = CategorySerializer(
    cates, many=True
)  # "cates" contains many records so many=True MUST HAVE

print(JSONRenderer().render(seri.data))
print("#########################")
qs = Category.objects.all()

try:
    item = qs.get(pk=7)
    print(CategorySerializer(item).data)
except Category.DoesNotExist:
    print("No PK found")
