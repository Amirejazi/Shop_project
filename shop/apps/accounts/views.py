from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyRegisterForm, UserLoginForm, ChangePasswordForm, RememberPasswordForm, UpdateProfileForm, ContactMessageForm
from django.contrib.auth import authenticate, login, logout
import utils
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order

from apps.payments.models import Payment


class RegisterUserView(View):
    template_name = 'accounts_app/registeruser.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            active_code = utils.create_random_code(5)
            user = CustomUser.objects.create_user(
                mobile_number=data['mobile_number'],
                active_code=active_code,
                password=data['password1']
            )
            utils.send_sms(data['mobile_number'], f"سلام به یوهول شاپ خوش آمدید :)\n کد فعال سازی حساب کاربری شما\nکد:{active_code}")
            request.session['user_session'] = {
                'active_code': str(active_code),
                'mobile_number': data['mobile_number'],
                'remember_password': False
            }
            messages.success(request, ' اطلاعات شما با موفقیت ثبت شد. کد فعال سازی را وارد کنید.', 'success')
            return redirect('accounts:verify')
        messages.error(request, 'خطا در انجام ثبت نام', 'danger')
        return render(request, self.template_name, {'form': form})


# =================================================================================================
class VerifyRegisterView(View):
    template_name = 'accounts_app/verify_register_code.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = VerifyRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VerifyRegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            if data['active_code'] == user_session['active_code']:
                user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
                if user_session['remember_password'] == False:
                    user.is_active = True
                    user.active_code = utils.create_random_code(5)
                    user.save()
                    messages.success(request, 'ثبت نام شما با موفقیت انجام شد :)', 'success')
                    return redirect('main:index')
                else:
                    user.active_code = utils.create_random_code(5)
                    user.save()
                    messages.success(request, 'رمز عبور جدید را وارد کنید', 'success')
                    return redirect('accounts:changePassword')
            else:
                messages.error(request, '!کد فعال سازی وارد شده اشتباه است', 'danger')
                return render(request, 'accounts_app/verify_register_code.html', {'form': form})
        messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
        return render(request, self.template_name, {'form': form})


# =================================================================================================
class LoginUserView(View):
    template_name = 'accounts_app/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data['mobile_number'], password=data['password'])
            if user is not None:
                user_db = CustomUser.objects.get(mobile_number=data['mobile_number'])
                if user_db.is_admin == False:
                    messages.success(request, 'ورود شما با موفقیت انجام شد:)', 'success')
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect('main:index')
                else:
                    messages.error(request, 'کاربر ادمین نمیتواند از اینجا وارد شود!', 'warning')
                    return render(request, self.template_name, {'form': form})
            else:
                messages.error(request, "شماره موبایل یا رمز عبور اشتباه است!", 'danger')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})


# ========================================================================================================
class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('main:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_data = request.session.get('shop_cart')
        logout(request)
        request.session['shop_cart'] = session_data
        return redirect('main:index')


# ========================================================================================================
class UserPanelView(LoginRequiredMixin, View):
    template_name = 'accounts_app/user_panel.html'
    
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'phone_number': user.mobile_number,
                'address': customer.address,
                'image': customer.image_name
            }
        except ObjectDoesNotExist:
            user_info = {
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }
        return render(request, self.template_name, {'user_info': user_info})
# =================================================================================================
@login_required
def show_last_order(request):
    orders = Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:4]
    return render(request, 'accounts_app/partial/show_last_orders.html', {'orders': orders})

# =================================================================================================
class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        image_url = ""
        try:
            customer = Customer.objects.get(user=user)
            initial_dict = {
                'mobile_number': user.mobile_number,
                'name': user.name,
                'family': user.family,
                'email': user.email,
                'phon_number': customer.phon_number,
                'address': customer.address,
            }
            image_url = customer.image_name
        except ObjectDoesNotExist:
            initial_dict = {
                'mobile_number': user.mobile_number,
                'name': user.name,
                'family': user.family,
                'email': user.email,
            }

        form = UpdateProfileForm(initial=initial_dict)
        if image_url:
            return render(request, 'accounts_app/update_profile.html', {'form': form, 'image_url': image_url})
        else:
            return render(request, 'accounts_app/update_profile.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            user.name = cd['name']
            user.family = cd['family']
            user.email = cd['email']
            user.save()
            try:
                customer = Customer.objects.get(user=user)
                customer.phon_number = cd['phon_number']
                customer.address = cd['address']
                customer.image_name = cd['image']
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=user,
                    phon_number=cd['phon_number'],
                    address=cd['address'],
                    image_name=cd['image']
                )
            messages.success(request, 'ویراییش پروفایل با موفقیت انجام شد :)')
            return redirect('accounts:user_panel')
        else:
            messages.error(request, 'اطلاعات وارد شده معتبر نمیباشد', 'danger')
            return render(request, 'accounts_app/update_profile.html', {'form': form})

# =================================================================================================
class ChangPasswordView(View):
    template_name = 'accounts_app/change_password.html'

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code = utils.create_random_code(5)
            user.save()
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد :)' ,'success')
            return redirect('accounts:login')
        else:
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})
# =================================================================================================
class RememberPasswordView(View):
    template_name = 'accounts_app/remember_password.html'

    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user = CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code = utils.create_random_code(5)
                user.active_code = active_code
                user.save()
                utils.send_sms(data['mobile_number'], f"کد تایید شماره موبایل شما \n  code :{ active_code } \nمی باشد.")
                request.session['user_session'] = {
                    'mobile_number': data['mobile_number'],
                    'active_code': str(active_code),
                    'remember_password': True
                }
                messages.info(request, 'جهت تغیر رمز عبور خود کد دریافتی را وارد کنید', 'info')
                return redirect('accounts:verify')
            except CustomUser.DoesNotExist:
                messages.error(request, 'این شماره موبایل موجود نمی باشد', 'danger')
                return render(request, self.template_name, {'form': form})
        else:
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})


# =========================================================================================================

class ChangPasswordInUserpanel(LoginRequiredMixin, View):
    template_name = 'accounts_app/change_password_in_userpanel.html'

    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user_session = request.session['user_session']
            user = CustomUser.objects.get(mobile_number=user_session['mobile_number'])
            user.set_password(data['password1'])
            user.active_code = utils.create_random_code(5)
            user.save()
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد :)' ,'success')
            return redirect('accounts:login')
        else:
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})


def show_user_payments(request):
    payments = Payment.objects.filter(customer_id=request.user.id).order_by('-register_date')
    return render(request, 'accounts_app/show_user_payments.html', {'payments': payments})

class ContactUsView(View):
    def get(self, request, *args, **kwargs):
        form = ContactMessageForm()
        return render(request, 'accounts_app/contact_us.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            msg = Message()
            msg.full_name = data['full_name']
            msg.email = data['email']
            msg.subject = data['subject']
            msg.message = data['message']
            msg.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد", "success")
            return redirect('accounts:contact_us')
        else:
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, 'accounts_app/contact_us.html', {'form': form})


def about_us(request):
    return render(request, 'accounts_app/about_us.html')
