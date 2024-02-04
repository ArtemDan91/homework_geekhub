from rest_framework import serializers

from api.cart.validators import validate_product_id_exists
from api.cart.validators import validate_positive_quantity


class CartProductDetailSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=50)
    product_description_name = serializers.CharField(max_length=255)
    sell_price = serializers.FloatField()
    quantity = serializers.IntegerField()
    products_total_cost = serializers.FloatField()


class CartSerializer(serializers.Serializer):
    cart_products = serializers.ListField()
    cart_total_amount = serializers.FloatField()
    cart_size = serializers.IntegerField()

    def to_representation(self, instance):
        cart_products_data = [CartProductDetailSerializer(cart_product).data for cart_product in instance['cart_products']]

        return {
            'cart_products': cart_products_data,
            'cart_total_amount': instance['cart_total_amount'],
            'cart_size': instance['cart_size'],
        }


class CartProductCreateSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=50, validators=[validate_product_id_exists])
    quantity = serializers.IntegerField(validators=[validate_positive_quantity])


class CartProductQuantityUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(validators=[validate_positive_quantity])







