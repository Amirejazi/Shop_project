from cProfile import label

from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='RePassword', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'email', 'name', 'family', 'gender')

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور با تکرار آن مغایرت دارد!')
        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# ======================================================================================
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور <a href='../password'> اینجا</a> کلیک کنید")

    class Meta:
        model = CustomUser
        fields = ('mobile_number', 'password', 'email', 'name', 'family', 'gender', 'is_active', 'is_admin')


# ======================================================================================
class UserRegisterForm(ModelForm):
    mobile_number = forms.CharField(label='شماره موبایل', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل را وارد کنید'}))
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور را وارد کنید'}))

    class Meta:
        model = CustomUser
        fields = ['mobile_number',]

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور با تکرار آن مغایرت دارد!')
        return pass2

# =======================================================================================
class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='کد دریافتی',
                                  error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد دریافتی را وارد کنید'}))

# =======================================================================================
class UserLoginForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل را وارد کنید'}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور را وارد کنید'}))

# =======================================================================================
class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'رمز عبور جدید را وارد کنید'}))
    password2 = forms.CharField(label='تکرار رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور جدید را وارد کنید'}))

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور با تکرار آن مغایرت دارد!')
        return pass2

# =======================================================================================
class RememberPasswordForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل را وارد کنید'}))


class UpdateProfileForm(forms.Form):
    mobile_number = forms.CharField(label='',
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره موبایل را وارد کنید', 'readonly': 'readonly'}))
    name = forms.CharField(label='', required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خود را وارد کنید'}))
    family = forms.CharField(label='', required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی خود را وارد کنید'}))
    email = forms.EmailField(label='', required=False,
                           widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل خود را وارد کنید'}))
    phon_number = forms.CharField(label='', required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره خود را وارد کنید'}))
    address = forms.CharField(label='', required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس خود را وارد کنید', 'rows': '2'}))
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control'}))


class ContactMessageForm(forms.Form):
    full_name = forms.CharField(label='',
                                  error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام شما'}))
    email = forms.EmailField(label='',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'آدرس ایمیل'}))
    subject = forms.CharField(label='',
                                  error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'موضوع'}))
    message = forms.CharField(label='',
                                error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}))