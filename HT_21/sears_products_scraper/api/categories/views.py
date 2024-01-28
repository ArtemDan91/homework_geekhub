from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from api.categories.serializers import CategorySerializer
from products.models import Category


class CategoryViewSetPagination(PageNumberPagination):
    page_size = 2


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryViewSetPagination
    http_method_names = ['get', 'delete']