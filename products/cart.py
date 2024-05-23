from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size, quantity=1, update_quantity=False):
        product_id = str(product.id)
        size_key = f"{product_id}_{size}"
        if size_key not in self.cart:
            self.cart[size_key] = {'quantity': 0, 'price': str(product.price), 'size': size}
        if update_quantity:
            self.cart[size_key]['quantity'] = quantity
        else:
            self.cart[size_key]['quantity'] += quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, size):
        product_id = str(product.id)
        size_key = f"{product_id}_{size}"
        if size_key in self.cart:
            del self.cart[size_key]
            self.save()

    def __iter__(self):
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            for key, value in cart.items():
                if key.startswith(str(product.id)):
                    value['product'] = product
                    yield value

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def update(self, product_id, size, quantity):
        size_key = f"{product_id}_{size}"
        if size_key in self.cart:
            self.cart[size_key]['quantity'] = quantity
            self.save()