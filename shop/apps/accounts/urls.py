from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', VerifyRegisterView.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('userpanel/', UserPanelView.as_view(), name='userpanel'),
    path('changePassword/', ChangPasswordView.as_view(), name='changePassword'),
    path('rememberPassword/', RememberPasswordView.as_view(), name='rememberPassword'),
]