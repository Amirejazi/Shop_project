# Generated by Django 4.1.6 on 2023-03-03 18:20

from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_brand_image_name_alter_product_image_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='featurevalue',
            options={'verbose_name': 'مقدار ویژگی', 'verbose_name_plural': 'مقادیر ویژگی ها'},
        ),
        migrations.AlterField(
            model_name='brand',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر برند'),
        ),
        migrations.AlterField(
            model_name='featurevalue',
            name='feature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feature_values', to='products.feature', verbose_name='ویژگی'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا'),
        ),
    ]
