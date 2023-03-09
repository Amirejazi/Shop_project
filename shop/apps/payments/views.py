from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.accounts.models import Customer
from django.conf import settings
import requests
import json


ZP_API_REQUEST = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/"+"{authority}/"

CallbackURL = 'http://127.0.0.1:8000/payments/verify/'

class ZarinPalPaymentView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        try:
            description = 'پرداخت از طریق درگاه زرین پال انجام شد'
            order = Order.objects.get(id=order_id)
            user = request.user
            payment = Payment.objects.create(
                order=order,
                customer=Customer.objects.get(user=user),
                amount=order.get_order_total_price(),
                description=description,
            )
            payment.save()
            request.session['payment_session'] = {
                'order_id': order.id,
                'payment_id': payment.id
            }
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": order.get_order_total_price(),
                "description": description,
                "callback_url": CallbackURL,
                'meta_data': {'mobile': user.mobile_number, 'email': user.email}
            }
            # set content length by data
            req_header = {'accept': 'application/json', 'content-type': 'application/json'}
            req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
            authority = req.json()['data']['authority']
            if len(req.json()['errors']) == 0:
                return redirect(ZP_API_STARTPAY.format(authority=authority))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse (f"Error code : {e_code}, Error message:{e_message}")
        except ObjectDoesNotExist:
            return redirect('orders:checkout_order', order_id)


class ZarinPalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['payment_session']['order_id']
        payment_id = request.session['payment_session']['payment_id']
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(id=payment_id)
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if t_status == "OK":
            req_header = {'accept': 'application/json', 'content-type': 'application/json'}
            req_data = {
                "merchant_id": settings.MERCHANT,
                "amount": order.get_order_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    order.is_finaly = True
                    order.save()

                    payment.is_finally = True
                    payment.status_code = t_status
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    return redirect('payments:show_verify_message', f"پرداخت با موفقیت انجام شد کد رهگیری شما:{str(req.json()['data']['ref_id'])}")
                elif t_status == 101:
                    order.is_finaly = True
                    order.save()

                    payment.is_finally = True
                    payment.status_code = t_status
                    payment.ref_id = str(req.json()['data']['ref_id'])
                    payment.save()
                    return redirect('payments:show_verify_message', f"پرداخت قبلا انجام شده کد رهگیری شما:{str(req.json()['data']['ref_id'])}")
                else:
                    payment.status_code = t_status
                    payment.save()
                    return redirect('payments:show_verify_message', f"خطا در فرایند پرداخت کد وضعیت :{t_status}")
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return redirect('payments:show_verify_message', f"خطا در فرایند پرداخت \nکد خطا :{e_code}\nپیام خطا:{e_message}")
        else:
            return redirect('payments:show_verify_message', f"خطا در فرایند پرداخت")


def show_verify_message(request, message):
    return render(request, 'payments_app/verify_message.html', {'message': message})

