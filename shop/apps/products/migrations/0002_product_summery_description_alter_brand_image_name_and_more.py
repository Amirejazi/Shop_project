# Generated by Django 4.1.6 on 2023-02-16 15:27

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='summery_description',
            field=ckeditor.fields.RichTextField(blank=True, default='', null=True, verbose_name='چکبده توضیحات'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر برند'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='productfeature',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_features', to='products.product', verbose_name='کالا'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه کالا'),
        ),
    ]
