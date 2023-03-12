from django.contrib import admin
from .models import Order, OrderDetail, PeymentType

@admin.register(PeymentType)
class PeymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'peyment_title')

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetail
    extra = 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'register_date', 'is_finaly', 'discount')
    inlines = [OrderDetailsInline]
