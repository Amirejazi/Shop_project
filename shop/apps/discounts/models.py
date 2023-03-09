from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True, verbose_name='کد کوپن')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')

    def __str__(self):
        return self.coupon_code

    class Meta:
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = "کوپن های تخفیف"
        db_table = 't_coupons'

# =================================================================================================
class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100, verbose_name='عنوان سبد خرید')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')

    def __str__(self):
        return self.discount_title

    class Meta:
        verbose_name = 'سبد تخفیف'
        verbose_name_plural = "سبد های تخفیف"
        db_table = 't_discount_basket'

# =============================================================================================================================
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, on_delete=models.CASCADE, related_name='discount_basket_details1', verbose_name='سبد تخفیف')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discount_basket_details2', verbose_name='کالا')

    class Meta:
        verbose_name = 'جزییات سبد تخفیف'
        db_table = 't_discount_basket_details'