# cart.py
from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, size, quantity=1, override_quantity=False):
        product_id = str(product.id)
        key = f"{product_id}_{size}"
        if key not in self.cart:
            self.cart[key] = {'quantity': 0, 'size': size, 'price': str(product.price)}
        if override_quantity:
            self.cart[key]['quantity'] = float(quantity)
        else:
            self.cart[key]['quantity'] += float(quantity)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_id, size):
        key = f"{product_id}_{size}"
        if key in self.cart:
            del self.cart[key]
            self.save()

    def __iter__(self):
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            for key in self.cart:
                if str(product.id) == key.split('_')[0]:
                    cart[key]['product'] = product
                    cart[key]['price'] = Decimal(cart[key]['price'])
                    cart[key]['total_price'] = cart[key]['price'] * cart[key]['quantity']
                    yield cart[key]

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_cart_items(self):
        product_ids = [key.split('_')[0] for key in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        cart_items = []
        for product in products:
            for key in self.cart:
                if str(product.id) == key.split('_')[0]:
                    cart_item = cart[key]
                    cart_item['product'] = product
                    cart_item['price'] = Decimal(cart_item['price'])
                    cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
                    cart_items.append(cart_item)
        return cart_items
