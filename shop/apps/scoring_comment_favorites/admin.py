from django.contrib import admin
from .models import *

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'commenting_user', 'approving_user', 'register_date', 'comment_parent', 'is_active')
    list_editable = ['is_active']

