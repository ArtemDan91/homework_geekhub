from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from api.products.serializers import ScrapedProductSerializer
from products.models import ScrapedProduct


class ScrapedProductViewSetPagination(PageNumberPagination):
    page_size = 10


class ScrapedProductViewSet(ModelViewSet):
    queryset = ScrapedProduct.objects.all()
    serializer_class = ScrapedProductSerializer
    lookup_field = 'product_id'
    pagination_class = ScrapedProductViewSetPagination
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


