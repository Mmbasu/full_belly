"""Defines urls for full belly app"""

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('', views.landing, name="landing"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('activate_account/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('check_login_button_status/', views.check_login_button_status, name='check_login_button_status'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
