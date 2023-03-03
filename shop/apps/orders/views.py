from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product

class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        return render(request, 'orders_app/shop_cart.html', {'shop_cart': shop_cart})

def show_shop_cart(request):
    shop_cart = ShopCart(request)
    total_price = shop_cart.calc_total_price()
    delivery = "25,000تومان"
    tax = int(0.09 * total_price)
    order_final_price = total_price + tax + 25000

    if total_price > 500000:
        delivery = "رایگان"
        order_final_price -= 25000

    context = {
        'shop_cart': shop_cart,
        "shop_cart_count": shop_cart.count,
        "total_price": total_price,
        "delivery": delivery,
        "tax": tax,
        "order_final_price": order_final_price
    }
    return render(request, 'orders_app/partial/show_shop_cart.html', context)


def add_to_shop_cart(request):
    product_id = request.GET.get('product_id')
    qty = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.add_to_shop_cart(product, qty)
    return HttpResponse(shop_cart.count)

def delete_from_shop_cart(request):
    product_id = request.GET.get('product_id')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')

def add_to_input_number(request):
    product_id = request.GET.get('id')
    qty = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.add_to_shop_cart(product, qty)
    return redirect('orders:show_shop_cart')
    # return HttpResponse(shop_cart.shop_cart[product_id]['price']*shop_cart.shop_cart[product_id]['qty'])

def sub_to_input_number(request):
    product_id = request.GET.get('id')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.delete_from_shop_cart_with_qty(product, 1)
    return redirect('orders:show_shop_cart')

def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return HttpResponse(shop_cart.count)
