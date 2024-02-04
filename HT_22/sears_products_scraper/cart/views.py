from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .cart import Cart
from .forms import EnterProductQuantityToCartForm


@login_required
def checkout_cart(request):
    cart = Cart(request)
    cart_added_products = cart.get_all_cart_products()
    return render(request, 'cart/cart_summary.html', {'cart_added_products': cart_added_products})


@login_required
def add_cart_data(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = EnterProductQuantityToCartForm(request.POST)
        if form.is_valid():
            product_id = request.POST.get('product_id')
            quantity = form.cleaned_data['quantity']
            cart.add_product_unit(product_id, quantity)
            total_cart_quantity = cart.__len__()
            return JsonResponse({'total_cart_quantity': total_cart_quantity})

    else:
        form = EnterProductQuantityToCartForm()
    return render(request, 'products/product_data.html',
                  {'form': form})


@login_required
def change_product_quantity(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        form_actions_dict = {
            'remove_product_unit': lambda: cart.remove_product_unit(product_id, 1),
            'add_product_unit': lambda: cart.add_product_unit(product_id, 1),
        }

        if action in form_actions_dict:
            form_actions_dict[action]()

        total_cart_quantity = cart.__len__()
        added_products_data = cart.get_cart_product_data(product_id)

        product_quantity = added_products_data['quantity']
        products_total_cost = added_products_data['products_total_cost']
        cart_total_amount = cart.get_cart_total_amount()

        return JsonResponse({'total_cart_quantity': total_cart_quantity, 'product_quantity': product_quantity,
                             'products_total_cost': products_total_cost, 'cart_total_amount': cart_total_amount})

    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def remove_cart_product(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart.remove_product(product_id)
        total_cart_quantity = cart.__len__()

        cart_total_amount = cart.get_cart_total_amount()

        return JsonResponse({'total_cart_quantity': total_cart_quantity, 'cart_total_amount': cart_total_amount})
    else:
        return JsonResponse({'error': 'Invalid request method'})


@login_required
def clear_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        cart.clear_cart()
        total_cart_quantity = cart.__len__()
        return JsonResponse({'total_cart_quantity': total_cart_quantity})
    else:
        return JsonResponse({'error': 'Invalid request method'})