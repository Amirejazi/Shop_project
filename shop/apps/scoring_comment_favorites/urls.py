from django.urls import path
from .views import *

app_name = 'sc-co-fa'
urlpatterns = [
    path('create_comment/<slug:slug>/', CommentView.as_view(), name='create_comment'),
]
