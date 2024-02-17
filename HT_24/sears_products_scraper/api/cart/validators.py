from rest_framework import serializers

from products.models import ScrapedProduct


def validate_product_id_exists(value):
    if not ScrapedProduct.objects.filter(product_id=value).exists():
        raise serializers.ValidationError("Product ID not found")
    return value


def validate_positive_quantity(value):
    if not isinstance(value, int) or value <= 0:
        raise serializers.ValidationError("Quantity must be a positive integer")
    return value