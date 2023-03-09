from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('discounts/', include('apps.discounts.urls', namespace='discounts')),
    path('payments/', include('apps.payments.urls', namespace='payments')),

    path('ckeditor', include('ckeditor_uploader.urls')),
    ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
