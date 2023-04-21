from django.db import models
from django.db.models import Sum, Avg
from django.urls import reverse
from utils import FileUpload
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from middlewares.middlewares import RequestMiddlewares


class Brand(models.Model):
    brand_title = models.CharField(max_length=100, verbose_name='نام برند')
    file_upload = FileUpload('images', 'brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to, blank=True, null=True, verbose_name='تصویر برند')
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.brand_title

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'
        db_table = 't_brands'


# ====================================================================================
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100, verbose_name='عنوان گروه کالا')
    file_upload = FileUpload('images', 'product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر گروه کالا')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال/غیرفعال')
    group_parent = models.ForeignKey('ProductGroup', null=True, blank=True, verbose_name='گروه والد',
                                     on_delete=models.CASCADE, related_name='groups')
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.group_title

    class Meta:
        verbose_name = 'گروه کالا ها'
        verbose_name_plural = "گروه های کالا ها"
        db_table = 't_product_group'


# =====================================================================================
class Feature(models.Model):
    feature_name = models.CharField(max_length=100, verbose_name='نام ویژگی')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='features_of_group')

    def __str__(self):
        return self.feature_name

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'
        db_table = 't_features'


# =======================================================================================
class Product(models.Model):
    product_name = models.CharField(max_length=500, verbose_name='نام کالا')
    summery_description = RichTextField(default="", config_name='default', blank=True, null=True, verbose_name='چکبده توضیحات')
    description = RichTextUploadingField(config_name='super', blank=True, null=True, verbose_name='توضیحات')
    file_upload = FileUpload('images', 'products')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا ها', related_name='products_of_group')
    brand = models.ForeignKey(Brand, null=True, on_delete=models.CASCADE, verbose_name='برند', related_name='products')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال/غیرفعال')
    register_date = models.DateField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateField(default=timezone.now, verbose_name='تاریخ انتشار')
    updated_date = models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروزرسانی')
    features = models.ManyToManyField(Feature, through='ProductFeature')
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.slug})


    def get_price_by_discount(self):
        list1 = []
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active == True and
                    dbd.discount_basket.start_date <= timezone.now() <= dbd.discount_basket.end_date):
                list1.append(dbd.discount_basket.discount)
        discount = 0
        if len(list1) > 0:
            discount = max(list1)
        return int(self.price - (self.price*discount/100))

    def get_number_in_warehouse(self):
        sum1 = self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum('qty'))
        sum2 = self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum('qty'))
        input = 0
        if sum1['qty__sum'] != None:
            input = sum1['qty__sum']
        output = 0
        if sum2['qty__sum'] != None:
            output = sum2['qty__sum']
        return input-output


    def get_user_score(self):
        request = RequestMiddlewares(get_response=None)
        request = request.thread_local.current_request
        score = 0
        user_score = self.scoring_product.filter(scoring_user=request.user)
        if user_score.count() > 0:
            score = user_score[0].score
        return round(score, 1)



    def get_average_score(self):
        avgScore = self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore == None:
            avgScore = 0
        return avgScore

    def get_user_favorite(self):
        request = RequestMiddlewares(get_response=None)
        request = request.thread_local.current_request
        flag = self.favorite_product.filter(favorite_user=request.user).exists()
        return flag


    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'
        db_table = 't_products'


# =============================================================================================
class FeatureValue(models.Model):
    value_title = models.CharField(max_length=200, verbose_name='عنوان مقدار')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, blank=True, null=True, verbose_name='ویژگی',
                                related_name='feature_values')

    def __str__(self):
        return f"{self.feature}: {self.value_title}"

    class Meta:
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی ها'
        db_table = 't_feature_value'


# =============================================================================================
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name='product_features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=100, verbose_name='مقدار ویژگی کالا')
    filter_value = models.ForeignKey(FeatureValue, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name='مقدار فیلتر ویژگی')

    def __str__(self):
        return f"{self.product} - {self.feature}: {self.value}"

    class Meta:
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'
        db_table = 't_product_feature'


# =============================================================================================
def upload_galleryProduct(instance, filename):
    return f"images/product_gallery/{instance.product.slug}/{filename}"


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='galley_images', verbose_name='کالا')
    image_name = models.ImageField(upload_to=upload_galleryProduct, verbose_name='تصویر')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصآویر'
        db_table = 't_galleryProduct'
