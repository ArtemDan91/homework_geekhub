from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

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
            category_name_slug = request.POST.get('category_name_slug')
            quantity = form.cleaned_data['quantity']
            cart.add_product_unit(product_id, quantity)
            return redirect(reverse('products:product_data', args=[category_name_slug, product_id]))
    else:
        form = EnterProductQuantityToCartForm()
    return render(request, 'products/product_data.html',
                  {'form': form})


@login_required
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
