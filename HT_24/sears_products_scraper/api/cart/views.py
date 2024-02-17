from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.cart.serializers import CartSerializer
from api.cart.serializers import CartProductCreateSerializer
from api.cart.serializers import CartProductDetailSerializer
from api.cart.serializers import CartProductQuantityUpdateSerializer
from cart.cart import Cart


class CartView(APIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart = Cart(request)

        serializer = CartSerializer({
            'cart_products': cart.get_all_cart_products(),
            'cart_total_amount': cart.get_cart_total_amount(),
            'cart_size': len(cart),
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CartProductCreateSerializer,
    )
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        serializer = CartProductCreateSerializer(data=request.data)

        if serializer.is_valid():
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity'))

            cart.add_product_unit(product_id, quantity)
            added_product_info = cart.get_cart_product_data(product_id)

            response_data = {
                'message': 'Product added to the cart successfully',
                **added_product_info
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        cart = Cart(request)

        if cart.cart:
            cart.clear_cart()

            return Response({'message': f'Cart has been cleared successfully'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': 'The cart is already empty'}, status=status.HTTP_400_BAD_REQUEST)


class CartProductView(APIView):
    serializer_class = CartProductDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id, *args, **kwargs):
        cart = Cart(request)

        if product_id in cart.cart:
            cart_product_data = cart.get_cart_product_data(product_id)
            serializer = CartProductDetailSerializer(cart_product_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'This product has not been added to the cart yet'}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=CartProductQuantityUpdateSerializer,
    )
    def patch(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        serializer = CartProductQuantityUpdateSerializer(data=request.data)

        if serializer.is_valid():
            quantity = request.data.get('quantity')

            if product_id in cart.cart:
                cart.update_product_quantity(product_id, quantity)
                udpated_cart_product_data = cart.get_cart_product_data(product_id)

                response_data = {
                    'message': 'Product quantity updated successfully',
                    **udpated_cart_product_data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'This product has not been added to the cart yet'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, *args, **kwargs):
        cart = Cart(request)

        if product_id in cart.cart:
            cart.remove_product(product_id)
            return Response({'message': f'Product {product_id} has been removed from the cart successfully'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'error': 'This product has not been added to the cart yet'},
                status=status.HTTP_400_BAD_REQUEST)

