from django.contrib import admin
from .models import *

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'customer', 'amount', 'is_finally', 'status_code', 'ref_id', 'register_date')
    ordering = ('register_date',)

