from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
    path('cheapest_products/', get_cheapest_products, name='cheapest_products'),
    path('last_products/', get_last_products, name='last_products'),
    path('most_selling_products/', get_most_selling_products, name='most_selling_products'),
    path('popular_groups/', get_popular_groups, name='popular_groups'),
    path('product_details/<slug:slug>/', ProductDetailsView.as_view(), name='product_details'),
    path('related_products/<slug:slug>/', get_related_products, name='related_products'),
    path('list_of_groups/', ProductGroupsView.as_view(), name='list_of_groups'),
    path('products_of_group/<slug:slug>/', ProductsOfGroupView.as_view(), name='products_of_group'),
    path('ajax_admin/', get_fliter_value_for_feature, name='filter_value_for_feature'),
    path('product_groups/', get_product_groups, name='product_groups_inFilter'),
    path('brands/<slug:slug>/', get_brands, name='brands'),
    path('features_filter/<slug:slug>/', get_features_for_filter, name='features_filter'),
    path('compare_list/', ShowCompareTableView.as_view(), name='show_compare_list'),
    path('compare_table/', compare_table, name='show_compare_table'),
    path('add_to_compare_list/', add_to_compare_list, name='add_to_compare_list'),
    path('delete_from_compare_list/', delete_from_compare_list, name='delete_from_compare_list'),
    path('categories_in_navbar/', categories_in_navbar, name='categories_in_navbar'),
    path('categories_in_mobile_menu/', categories_in_mobile_menu, name='categories_in_mobile_menu'),
]
