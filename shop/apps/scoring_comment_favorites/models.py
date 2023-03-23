from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments_of_product', verbose_name='کالا')
    commenting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_writer', verbose_name='کاربر نظر دهنده')
    approving_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment_approver', verbose_name='کاربر تایید کننده نظر', null=True, blank=True)
    comment_text = models.TextField(verbose_name='متن نظر')
    register_date = models.DateField(auto_now_add=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')
    comment_parent = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='comments_child', null=True, blank=True, verbose_name='والد نظر')

    def __str__(self):
        return f"{self.product}  {self.commenting_user}"

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'
        db_table = 't_comments'



