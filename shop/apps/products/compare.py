from apps.products.models import Product


class CompareProduct:
    def __init__(self, request):
        self.session = request.session
        compare_product = self.session.get('compare_product')
        if not compare_product:
            compare_product = self.session['compare_product'] = []
        self.compare_product = compare_product
        self.count = len(self.compare_product)

    # ===========================================================================
    def __iter__(self):
        compare_product = self.compare_product.copy()
        for item in compare_product:
            yield item

    def add_to_compare_product(self, product_id):
        product_id = int(product_id)
        if product_id not in self.compare_product:
            self.compare_product.append(product_id)
        self.count = len(self.compare_product)
        self.session.modified = True

    def delete_from_compare_product(self, product_id):
        self.compare_product.remove(int(product_id))
        self.session.modified = True

    def clear_compare_product(self):
        del self.compare_product
        self.session.modified = True
