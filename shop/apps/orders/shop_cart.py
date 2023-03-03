from apps.products.models import Product

class ShopCart:
    def __init__(self, request):
        self.session = request.session
        temp = self.session.get('shop_cart')
        if not temp:
            temp = self.session['shop_cart'] = {}
        self.shop_cart = temp
        self.count = len(self.shop_cart.keys())

    def add_to_shop_cart(self, product, qty):
        product_id = str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id] = {"qty": 0, "price": product.price}
        self.shop_cart[product_id]["qty"] += int(qty)
        self.count = len(self.shop_cart.keys())
        self.session.modified = True

    def delete_from_shop_cart(self, product):
        product_id = str(product.id)
        del self.shop_cart[product_id]
        self.session.modified = True

    def delete_from_shop_cart_with_qty(self, product, qty):
        product_id = str(product.id)
        if product_id in self.shop_cart:
            if self.shop_cart[product_id]["qty"] > 1:
                self.shop_cart[product_id]["qty"] -= int(qty)
            else:
                del self.shop_cart[product_id]
        self.session.modified = True

    def __iter__(self):
        list_id = self.shop_cart.keys()
        products = Product.objects.filter(id__in=list_id)
        temp = self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]['product'] = product

        for item in temp.values():
            item['total_price'] = item['price'] * item['qty']
            yield item

    def calc_total_price(self):
        sum = 0
        for item in self.shop_cart.values():
            sum += item['qty']*item['price']
        return sum


