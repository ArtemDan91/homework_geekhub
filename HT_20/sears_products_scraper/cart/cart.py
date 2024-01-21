from django.shortcuts import get_object_or_404
from products.models import ScrapedProduct


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add_product_unit(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = quantity
        else:
            self.cart[product_id] += quantity
        self.save()

    def remove_product_unit(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] -= quantity
            self.save()

    def remove_product(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear_cart(self):
        self.cart.clear()
        self.save()

    def __len__(self):
        return sum(self.cart.values())

    def get_all_cart_products(self):
        cart_added_products = []
        for product_id, quantity in self.cart.items():
            product = get_object_or_404(ScrapedProduct, product_id=product_id)
            products_total_cost = round(float(product.sell_price) * quantity,
                                        2)
            cart_added_products.append(
                {
                    'product_id': product_id,
                    'product_name': product.product_description_name,
                    'sell_price': product.sell_price,
                    'quantity': quantity,
                    'products_total_cost': products_total_cost
                }
            )
        return cart_added_products

    def get_cart_total_amount(self):
        total_cart_amount = 0
        products_ids = self.cart.keys()
        products = ScrapedProduct.objects.filter(product_id__in=products_ids)

        for id, quantity in self.cart.items():
            for product in products:
                if product.product_id == id:
                    total_cart_amount += float(product.sell_price) * quantity

        return round(total_cart_amount, 2)

    def save(self):
        self.session.modified = True
