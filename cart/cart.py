from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    # starts the cart
    def __init__(self, request):
        self.session = request.session
        # loads the cart from the current session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Iterate over the items in the cart and get the products from the database.
    def __iter__(self):
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    # Returns the sum of the quantities of all items in the cart.
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # Add a product to the cart or update its quantity.
    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # mark the session as modified to save it
        self.session.modified = True

    # Remove a product from the cart.
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # Calculates the total cost of the items in the cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    # clears the cart session by removing it
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()