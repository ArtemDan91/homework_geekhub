from rest_framework import serializers

from products.models import ScrapedProduct


class ScrapedProductSerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    category = serializers.CharField(source='category.name', max_length=255, read_only=True)

    class Meta:
        model = ScrapedProduct
        fields = (
            'product_id',
            'product_description_name',
            'sell_price',
            'category',
            'url'
        )
