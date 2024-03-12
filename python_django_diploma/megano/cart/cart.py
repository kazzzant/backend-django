from django.conf import settings


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item_id, count=1):
        product_id = str(item_id)
        if product_id not in self.cart:
            self.cart[product_id] = {"count": count}
        else:
            self.cart[product_id]["count"] += count
            if self.cart[product_id]["count"] < 1:
                self.remove(product_id)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
