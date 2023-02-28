from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from admin_decorators import short_description, order_field
from django.db.models import Q
from django.db.models.aggregates import Count
from django.contrib.admin.actions import delete_selected
from django.utils.html import format_html

from .models import *
from django.core import serializers
from django.http import HttpResponse


# Brand Admin =============================================================================
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title', 'image_tag', 'slug')
    list_filter = ('brand_title',)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)

    @short_description('تصویر برند')
    def image_tag(self, obj):
        if obj.image_name != "":
            return format_html(f'<img src="{obj.image_name.url}" style="width: 100px; height:100px;" />')
        return format_html('<img src="" style="width: 100px; height:100px;" alt="فاقد تصویر" />')



# productGroup Admin ====================================================================================
def deActive_productGroup(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} گروه کالا غیرفعال شدند  '
    modeladmin.message_user(request, message)


def Active_productGroup(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} گروه کالا فعال شدند  '
    modeladmin.message_user(request, message)


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    extra = 1


class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات'
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        sub_groups = ProductGroup.objects.filter(~Q(group_parent=None))
        groups = set([item.group_parent for item in sub_groups])
        return [(item.id, item.group_title) for item in groups]

    def queryset(self, request, queryset):
        if self.value() != None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset


@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title', 'image_tag', 'group_parent', 'slug', 'is_active', 'count_sub_group', 'count_product_group')
    list_filter = (GroupFilter, 'is_active')
    search_fields = ('group_title',)
    ordering = ('group_parent', 'group_title',)
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [deActive_productGroup, Active_productGroup, export_as_json]
    list_editable = ['is_active']

    @short_description('تصویر گروه')
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image_name.url}" style="width: 125px; height:100px;" />')

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductGroupAdmin, self).get_queryset(*args, **kwargs)
        qs = qs.annotate(sub_group=Count('groups'))
        qs = qs.annotate(product_group=Count('products_of_group'))
        return qs

    @short_description('تعداد زیرگروه ها')
    @order_field('sub_group')
    def count_sub_group(self, obj):
        return obj.sub_group

    @short_description('تعداد کالا ها')
    @order_field('product_group')
    def count_product_group(self, obj):
        return obj.product_group

    deActive_productGroup.short_description = 'غیرفعال کردن گروه های انتخاب شده'
    Active_productGroup.short_description = 'فعال کردن گروه های انتخاب شده'
    delete_selected.short_description = 'حذف گروه های انتخاب شده'
    export_as_json.short_description = 'خروجی جیسون برای گروه های انتخاب شده'


# ===============================================================================================
def deActive_product(modeladmin, request, queryset):
    res = queryset.update(is_active=False)
    message = f'تعداد {res} کالا غیرفعال شدند  '
    modeladmin.message_user(request, message)


def Active_product(modeladmin, request, queryset):
    res = queryset.update(is_active=True)
    message = f'تعداد {res} کالا فعال شدند  '
    modeladmin.message_user(request, message)


class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 4

    class Media:
        css = {
            'all': ('css/admin_style.css',)
        }

        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )


class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'image_tag', 'brand', 'price', 'updated_date', 'display_product_group', 'slug', 'is_active')
    list_filter = ('product_group', 'brand')
    search_fields = ('product_name', 'product_group', 'brand')
    ordering = ('updated_date', 'product_name',)
    actions = [deActive_product, Active_product, export_as_json]
    inlines = [ProductFeatureInlineAdmin, ProductGalleryInlineAdmin]
    list_editable = ['is_active']

    deActive_productGroup.short_description = 'غیرفعال کردن کالا های انتخاب شده'
    Active_productGroup.short_description = 'فعال کردن کالا های انتخاب شده'

    @short_description('تصویر کالا')
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image_name.url}" style="width: 125px; height:100px;" />')

    def display_product_group(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])

    display_product_group.short_description = 'گروه های کالا'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets = (
        ('اطلاعات محصول', {'fields': (
            'product_name',
            'image_name',
            'product_group',
            ('brand', 'is_active'),
            'price',
            'slug',
            'summery_description',
            'description',
        )}),
        ('تاریخ و زمان', {'fields': (
            'published_date',
        )})
    )


# ======================================================================================
class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'display_groups', 'display_feature_values')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInline]

    @short_description('گروه های دارای این ویژگی')
    def display_groups(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])

    @short_description('مقادیر ممکن برای این ویژگی')
    def display_feature_values(self, obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_values.all()])

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            kwargs['queryset'] = ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)