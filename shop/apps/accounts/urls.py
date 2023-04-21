from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify/', VerifyRegisterView.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('user_panel/', UserPanelView.as_view(), name='user_panel'),
    path('show_last_orders/', show_last_order, name='show_last_orders'),
    path('update_profile_view/', UpdateProfileView.as_view(), name='update_profile_view'),
    path('changePassword/', ChangPasswordView.as_view(), name='changePassword'),
    path('rememberPassword/', RememberPasswordView.as_view(), name='rememberPassword'),
    path('change_password_in_userpanel/', ChangPasswordInUserpanel.as_view(), name='change_password_in_userpanel'),
    path('show_user_payments/', show_user_payments, name='show_user_payments'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),
    path('about_us/', about_us, name='about_us'),
]