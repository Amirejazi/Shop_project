from django.contrib import admin
from .models import *

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_code', 'discount', 'start_date', 'end_date', 'is_active')
    ordering = ('is_active',)

class DiscountBasketDetailInline(admin.TabularInline):
    model = DiscountBasketDetails
    extra = 3

@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display = ('discount_title', 'discount', 'start_date', 'end_date', 'is_active')
    ordering = ('is_active',)
    inlines = [DiscountBasketDetailInline]
