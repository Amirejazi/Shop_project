from django.contrib import admin
from .models import Order, OrderDetail, PeymentType, OrderState

@admin.register(PeymentType)
class PeymentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'peyment_title')

class OrderDetailsInline(admin.TabularInline):
    model = OrderDetail
    extra = 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_state', 'register_date', 'is_finaly', 'discount')
    ordering = ('register_date',)
    inlines = [OrderDetailsInline]


@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_state_title')
