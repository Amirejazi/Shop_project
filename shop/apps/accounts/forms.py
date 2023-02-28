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
