from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from apps.accounts.models import Customer
from .models import Order, OrderDetail, PeymentType
from .forms import OrderForm
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupon
from django.db.models import Q


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

# ====================================================================================================
class CreditOrderView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
        except ObjectDoesNotExist:
            customer = Customer.objects.create(user=request.user)

        order = Order.objects.create(customer=customer, peyment_type=get_object_or_404(PeymentType, id=1))

        shop_cart = ShopCart(request)
        for item in shop_cart:
            OrderDetail.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                qty=item['qty'],
            )
        return redirect('orders:checkout_order', order.id)


class CheckOutOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        user = request.user
        customer = get_object_or_404(Customer, user=user)
        shop_cart = ShopCart(request)
        order = get_object_or_404(Order, id=order_id)

        total_price = shop_cart.calc_total_price()
        delivery = "25,000تومان"
        tax = int(0.09 * total_price)
        order_final_price = total_price + tax + 25000

        if total_price > 500000:
            delivery = "رایگان"
            order_final_price -= 25000

        if order.discount > 0:
            order_final_price = order_final_price-(order_final_price*order.discount/100)
        data = {
            'name': user.name,
            'family': user.family,
            'email': user.email,
            'phone_number': customer.phon_number,
            'address': customer.address,
            'description': order.description,
            'peyment_type': order.peyment_type,
        }

        form = OrderForm(data)
        form_coupon = CouponForm()
        context = {
            'shop_cart': shop_cart,
            'total_price': total_price,
            'tax': tax,
            'delivery': delivery,
            'order_final_price': order_final_price,
            'order': order,
            'form': form,
            'form_coupon': form_coupon
        }
        return render(request, 'orders_app/checkout.html', context)

    def post(self, request, order_id):
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                order = Order.objects.get(id=order_id)
                order.description =cd['description']
                order.peyment_type = PeymentType.objects.get(id=cd['peyment_type'])
                order.save()

                user = request.user
                user.name = cd['name']
                user.family = cd['family']
                user.email = cd['email']
                user.save()

                customer = Customer.objects.get(user=user)
                customer.address = cd['address']
                customer.phon_number = cd['phone_number']
                customer.save()

                # messages.success(request, 'موفقیت اعمال شد :)')
                return redirect('payments:zarinpal_payment', order_id)
            except ObjectDoesNotExist:
                messages.error(request, 'فاکتوری با این مشخصات یافت نشد !', 'danger')
                return redirect('orders:checkout_order', order_id)



class ApplyCoupon(View):
    def post(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        form_coupon = CouponForm(request.POST)
        if form_coupon.is_valid():
            cd = form_coupon.cleaned_data
            coupon_code = cd['coupon_code']
            coupon = Coupon.objects.filter(
                Q(coupon_code=coupon_code) &
                Q(is_active=True) &
                Q(start_date__lte=timezone.now()) &
                Q(end_date__gte=timezone.now())
            )

            discount = 0
            try:
                order = Order.objects.get(id=order_id)
                if coupon:
                    discount = coupon[0].discount
                    order.discount = discount
                    order.save()
                    messages.success(request, 'کد تخفیف با موفقیت اعمال شد :)', 'success')
                    return redirect('orders:checkout_order', order_id)
                else:
                    order.discount = discount
                    order.save()
                    messages.error(request, 'کد وارد شده معتبر نیست !', 'danger')
            except ObjectDoesNotExist:
                messages.error(request, 'سفارش موجود نیست!', 'danger')
            return redirect('orders:checkout_order', order_id)

