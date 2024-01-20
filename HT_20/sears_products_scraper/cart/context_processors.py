from .cart import Cart


def cart_products_count_context(request):
    cart = Cart(request)
    total_cart_quantity = sum(cart.cart.values())
    return {'total_cart_quantity': total_cart_quantity}
