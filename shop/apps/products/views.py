from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .compare import CompareProduct
from .filters import ProductFilter
from .models import ProductGroup, Product, FeatureValue, Brand
from django.db.models import Q, Count, Min, Max, Sum
from apps.warehouses.models import WarehouseType

# ارزان ترین محصولات
def get_cheapest_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('price')[:6]
    product_groups = ProductGroup.objects.filter(Q(is_active=True) & ~Q(group_parent=None))[:4]
    context = {
        'product_groups': product_groups,
        'products': products
    }
    return render(request, 'products_app/partial/cheapest_products.html', context)


# محصولات جدید
def get_last_products(request, *args, **kwargs):
    products = Product.objects.filter(is_active=True).order_by('-published_date')[:6]
    product_groups = ProductGroup.objects.filter(Q(is_active=True) & ~Q(group_parent=None))[:4]
    context = {
        'product_groups': product_groups,
        'products': products
    }
    return render(request, 'products_app/partial/last_products.html', context)

# پرفروش ترین محصولات
def get_most_selling_products(request):
    products = Product.objects.filter(Q(is_active=True) & Q(warehouse_products__warehouse_type=WarehouseType.objects.get(id=2)))\
                   .annotate(count=Sum('warehouse_products__qty'))\
                   .order_by('-count')[:7]

    big_cart_product = products[0]  # پرفروش ترین محصول رو برای اون کارت بزگه تو تمپلیت جدا میکنیم
    products = products[1:7]
    return render(request, 'products_app/partial/most_selling_products.html', {'products': products, 'product': big_cart_product})

# دسته های محبوب
def get_popular_groups(request, *args, **kwargs):
    product_groups = ProductGroup.objects.filter(is_active=True).annotate(count=Count('products_of_group')).order_by('-count')[:6]
    context = {
        'product_groups': product_groups,
    }
    return render(request, 'products_app/partial/popular_groups.html', context)


# جزییات محصول
class ProductDetailsView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        features = product.product_features.all()[:4]
        all_features = product.product_features.all()
        context = {
            'product': product,
            'features': features,
            'all_features': all_features,
        }
        if product.is_active:
            return render(request, 'products_app/product_details.html', context)


# محصولات مرتبط
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs['slug'])
    related_products = []
    for group in current_product.product_group.all():
        related_products.extend(group.products_of_group.filter(Q(is_active=True) & ~Q(id=current_product.id)))
    return render(request, 'products_app/partial/related_products.html', {'related_products': related_products})


# لیست کلیه محصولات
class ProductGroupsView(View):
    def get(self, request, *args, **kwargs):
        main_product_groups = ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
        return render(request, 'products_app/list_of_groups.html', {'main_product_groups': main_product_groups})


# لیست محصولات هر گروه
class ProductsOfGroupView(View):
    def get(self, request, *args, **kwargs):
        current_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
        products = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))

        res_aggre = products.aggregate(min=Min('price'), max=Max('price'))

        # price_filter
        filter = ProductFilter(request.GET, products)
        products = filter.qs

        # brand_filter
        brands_filter = request.GET.getlist('brand')
        if brands_filter:
            products = products.filter(brand__id__in=brands_filter)

        # features_filter
        features_filter = request.GET.getlist('feature')
        if features_filter:
            products = products.filter(product_features__filter_value__id__in=features_filter).distinct()

        # sort_type
        sort_type = request.GET.get('sort_type')
        if not sort_type:
            sort_type = "0"
        if sort_type == '1':
            products = products.order_by('price')
        elif sort_type == '2':
            products = products.order_by('-price')

        # paginate
        product_per_page = 2
        number_show = request.GET.get('number_show')
        if not number_show:
            if request.session.get('number_show') is not None:
                product_per_page = request.session['number_show']
                number_show = str(product_per_page)
            else:
                number_show = "4"
                product_per_page = 4
        elif number_show == "4":
            product_per_page = 4
            request.session['number_show'] = 4
        elif number_show == "6":
            product_per_page = 6
            request. session['number_show'] = 6
        elif number_show == "9":
            product_per_page = 9
            request.session['number_show'] = 9

        paginator = Paginator(products, product_per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        products_count = products.count()


        context = {
            'current_group': current_group,
            'products': products,
            'res_aggre': res_aggre,
            'products_count': products_count,
            'page_obj': page_obj,
            'sort_type': sort_type,
            'number_show': number_show,
        }
        return render(request, 'products_app/products_of_group.html', context)


# لیست گروه محصولات درفیلتر
def get_product_groups(request):
    product_groups = ProductGroup.objects.annotate(count=Count('products_of_group')) \
                         .filter(Q(is_active=True) & ~Q(count=0)) \
                         .order_by('-count')[:7]
    return render(request, 'products_app/partial/product_groups.html', {'product_groups': product_groups})


# لیست برند برای فیلتر
def get_brands(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    brand_list_id = product_group.products_of_group.filter(is_active=True).values('brand_id')
    brands = Brand.objects.filter(pk__in=brand_list_id) \
        .annotate(count=Count('products')) \
        .filter(~Q(count=0)) \
        .order_by('-count')
    return render(request, 'products_app/partial/brands.html', {'brands': brands})


#  لیست های دیگر فیلتر ها برحسب مقادیر ویژگی های کالاهای درون گروه
def get_features_for_filter(request, *args, **kwargs):
    product_group = get_object_or_404(ProductGroup, slug=kwargs['slug'])
    feature_list = product_group.features_of_group.all()
    feature_dict = dict()
    for feature in feature_list:
        feature_dict[feature] = feature.feature_values.all()
    return render(request, 'products_app/partial/features_filter.html', {'feature_dict': feature_dict})


# =====================================================================================
# dropdown in adminpanel
def get_fliter_value_for_feature(request):
    if request.method == "GET":
        feature_id = request.GET['feature_id']
        feature_values = FeatureValue.objects.filter(feature=feature_id)
        res = {fv.value_title: fv.id for fv in feature_values}
        return JsonResponse(data=res, safe=False)


# صفحه اصلی مقایسه : نمایش کالا های اضافه شده به لیست
class ShowCompareTableView(View):
    def get(self, request, *args, **kwargs):
        compare_list = CompareProduct(request)
        return render(request, 'products_app/compare_list.html', {'compare_list': compare_list})


# نمایش جدول کالا های لیست مقایسه
def compare_table(request):
    compare_list = CompareProduct(request)

    products = []
    for product_id in compare_list.compare_product:
        product = Product.objects.get(id=product_id)
        products.append(product)

    features = []
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
    context = {
        'products': products,
        'features': features
    }
    return render(request, 'products_app/partial/compare_table.html', context)


def add_to_compare_list(request):
    product_id = request.GET['product_id']
    compare_list = CompareProduct(request)
    compare_list.add_to_compare_product(product_id)
    return HttpResponse("کالا به لیست مقایسه اضافه شد")

def delete_from_compare_list(request):
    product_id = request.GET['product_id']
    compare_list = CompareProduct(request)
    compare_list.delete_from_compare_product(product_id)
    return redirect('products:show_compare_table')


def categories_in_navbar(request):
    main_groups = ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))[:6]
    return render(request, 'products_app/partial/categories_in_navbar.html', {'main_groups': main_groups})

def categories_in_mobile_menu(request):
    main_groups = ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
    return render(request, 'products_app/partial/categories_in_mobile_menu.html', {'main_groups': main_groups})