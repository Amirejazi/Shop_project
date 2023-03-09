from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
import uuid
#================================================================
class PeymentType(models.Model):
    peyment_title = models.CharField(max_length=50, verbose_name='نوع پرداخت')

    def __str__(self):
        return self.peyment_title

    class Meta:
        verbose_name = 'نوع پرداخت'
        verbose_name_plural = 'انواع روش پرداخت'
        db_table = "t_peyment_types"
# =================================================================
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders", verbose_name="مشتری")
    register_date = models.DateField(default=timezone.now, verbose_name='تاریخ درج سفارش')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ ویرایش سفارش')
    is_finaly = models.BooleanField(default=False, verbose_name="نهایی شده")
    order_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='کد تولیدی یرای سفارش')
    discount = models.IntegerField(blank=True, null=True, default=0, verbose_name='تخفیف روی سفارش')
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    peyment_type = models.ForeignKey(PeymentType, blank=True, null=True, default=None, on_delete=models.CASCADE, related_name='peyment_types', verbose_name="نوع پرداخت")

    def get_order_total_price(self):
        sum = 0
        for item in self.orders_details1.all():
            sum += item.product.get_price_by_discount()*int(item.qty)
        delivery = 25000
        if sum > 500000:
            delivery = 0
        tax = 0.09*sum
        final_price = sum+tax+delivery
        return int(final_price-(final_price*self.discount/100))


    def __str__(self):
        return f"{self.customer}  {self.id}  {self.is_finaly}"

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        db_table = "t_orders"

# ======================================================================================================================
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders_details1', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders_details1', verbose_name='کالا')
    qty = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت در فاکتور')

    def __str__(self):
        return f"{self.order} {self.product}  {self.qty} {self.price}"

    class Meta:
        verbose_name = " جزییات سفارش"
        db_table = "t_Order_details"
