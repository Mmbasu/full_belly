"""Defines urls for full belly app"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('activate_account/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('my_password_reset_confirm/<uidb64>/<token>/', views.my_password_reset_confirm,
         name='my_password_reset_confirm')
]
