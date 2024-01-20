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

    def save(self):
        self.session.modified = True
