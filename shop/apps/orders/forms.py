from django import forms
from .models import PeymentType

class OrderForm(forms.Form):
    name = forms.CharField(label="",
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
                           error_messages={'required': "این فیلد نمیتواند خالی باشد!"})

    family = forms.CharField(label="",
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
                             error_messages={'required': "این فیلد نمیتواند خالی باشد!"})

    email = forms.CharField(label="",
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' ایمیل'}),
                            error_messages={'required': "این فیلد نمیتواند خالی باشد!"})

    phone_number = forms.CharField(label="",
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'تلفن'}),
                                   required=False)

    address = forms.CharField(label="",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'آدرس', 'rows': '2'}),
                              error_messages={'required': "این فیلد نمیتواند خالی باشد!"})

    description = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'توضیحات', 'rows': '4'}),
                                  required=False)
    peyment_type = forms.ChoiceField(label="",
                                     choices=[(item.id, item) for item in PeymentType.objects.all()],
                                     widget=forms.RadioSelect())