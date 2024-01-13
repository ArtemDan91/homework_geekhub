from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from products.models import ScrapedProduct

def checkout_cart(request):
    cart = Cart(request)
    session_data = cart.cart
    cart_added_products = []
    total_cart_amount = 0
    for product_id, quantity in session_data.items():
        product = get_object_or_404(ScrapedProduct, product_id=product_id)
        products_total_cost = round(float(product.sell_price) * quantity, 2)
        cart_added_products.append(
            {
                'product_id': product_id,
                'product_name': product.product_description_name,
                'sell_price': product.sell_price,
                'quantity': quantity,
                'products_total_cost': products_total_cost
            }
        )
        total_cart_amount += products_total_cost
    return render(request, 'cart/cart_summary.html', {'cart_added_products': cart_added_products, 'total_cart_amount': round(total_cart_amount, 2)})


def update_cart_data(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        form_actions_dict = {
            'remove_product_unit': lambda: cart.remove_product_unit(product_id, 1),
            'add_product_unit': lambda: cart.add_product_unit(product_id, 1),
            'remove_product': lambda: cart.remove_product(product_id),
            'clear_cart': lambda: cart.clear_cart(),
        }

        if action in form_actions_dict:
            form_actions_dict[action]()

    return redirect('cart:checkout_cart')
