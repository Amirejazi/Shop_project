from django.contrib import admin
from .models import *

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse_type_title',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouse_type', 'user_registered', 'product', 'qty', 'price', 'register_date')
    ordering = ('register_date',)
