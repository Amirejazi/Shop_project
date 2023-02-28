class ShopCart:
    def __int__(self, request):
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
        self.shop_cart[product_id]["qty"] += qty
        self.count = len(self.shop_cart.keys())
        self.session.modified = True

    def delete_from_shop_cart(self, product):
        product_id = str(product.id)
        del self.shop_cart[product_id]
