# Generated by Django 4.1.6 on 2023-02-11 23:08

import apps.products.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_title', models.CharField(max_length=100, verbose_name='نام برند')),
                ('image_name', models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر برند')),
                ('slug', models.SlugField(max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
                'db_table': 't_brands',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=100, verbose_name='نام ویژگی')),
            ],
            options={
                'verbose_name': 'ویژگی',
                'verbose_name_plural': 'ویژگی ها',
                'db_table': 't_features',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=500, verbose_name='نام کالا')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='وضعیت فعال/غیرفعال')),
                ('register_date', models.DateField(auto_now_add=True, verbose_name='تاریخ درج')),
                ('published_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('updated_date', models.DateField(auto_now=True, verbose_name='تاریخ آخرین بروزرسانی')),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.brand', verbose_name='برند')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالا ها',
                'db_table': 't_products',
            },
        ),
        migrations.CreateModel(
            name='ProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_title', models.CharField(max_length=100, verbose_name='عنوان گروه کالا')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='وضعیت فعال/غیرفعال')),
                ('slug', models.SlugField(max_length=100, null=True)),
                ('group_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='products.productgroup', verbose_name='گروه والد')),
            ],
            options={
                'verbose_name': 'گروه کالا ها',
                'verbose_name_plural': 'گروه های کالا ها',
                'db_table': 't_product_group',
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.ImageField(upload_to=apps.products.models.upload_galleryProduct, verbose_name='تصویر')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصآویر',
                'db_table': 't_galleryProduct',
            },
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100, verbose_name='مقدار ویژگی کالا')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.feature', verbose_name='ویژگی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'ویژگی محصول',
                'verbose_name_plural': 'ویژگی های محصولات',
                'db_table': 't_product_feature',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.ManyToManyField(through='products.ProductFeature', to='products.feature'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_group',
            field=models.ManyToManyField(related_name='products_of_group', to='products.productgroup', verbose_name='گروه کالا ها'),
        ),
        migrations.AddField(
            model_name='feature',
            name='product_group',
            field=models.ManyToManyField(related_name='features_of_group', to='products.productgroup', verbose_name='گروه کالا'),
        ),
    ]
