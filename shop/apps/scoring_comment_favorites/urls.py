from django.urls import path
from .views import *

app_name = 'sc-co-fa'
urlpatterns = [
    path('create_comment/<slug:slug>/', CommentView.as_view(), name='create_comment'),
    path('add_score/', add_score, name='add_score'),
    path('add_to_favorite/', add_to_favorite, name='add_to_favorite'),
    path('status_of_favorite/', status_of_favorite, name='status_of_favorite'),
    path('remove_from_favorite/', remove_from_favorite, name='remove_from_favorite'),
    path('user_favorites/', UserFavoriteView.as_view(), name='user_favorites'),
]
