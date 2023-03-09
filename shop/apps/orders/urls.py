from django.urls import path
from .views import *

app_name = 'orders'
urlpatterns = [
    path('shop_cart/', ShopCartView.as_view(), name='shop_cart'),
    path('show_shop_cart/', show_shop_cart, name='show_shop_cart'),
    path('add_to_input_number/', add_to_input_number, name='add_to_input_number'),
    path('sub_to_input_number/', sub_to_input_number, name='sub_to_input_number'),
    path('add_to_shop_cart/', add_to_shop_cart, name='add_to_shop_cart'),
    path('delete_from_shop_cart/', delete_from_shop_cart, name='delete_from_shop_cart'),
    path('status_of_shop_cart/', status_of_shop_cart, name='status_of_shop_cart'),
    path('credit_order/', CreditOrderView.as_view(), name='credit_order'),
    path('checkout_order/<int:order_id>/', CheckOutOrderView.as_view(), name='checkout_order'),
    path('apply_coupon/<int:order_id>/', ApplyCoupon.as_view(), name='apply_coupon'),
]
