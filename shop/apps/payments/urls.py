from django.urls import path
from .views import *

app_name = 'payments'
urlpatterns = [
    path('zarinpal_payment/<int:order_id>/', ZarinPalPaymentView.as_view(), name='zarinpal_payment'),
    path('verify/', ZarinPalPaymentVerifyView.as_view(), name='zarinpal_payment_verify'),
    path('show_verify_message/<str:message>/', show_verify_message, name='show_verify_message'),
]
