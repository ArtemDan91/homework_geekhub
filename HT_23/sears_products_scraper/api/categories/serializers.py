from rest_framework import serializers

from api.products.serializers import ScrapedProductSerializer
from products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    products = ScrapedProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'name_slug',
            'products',
        )