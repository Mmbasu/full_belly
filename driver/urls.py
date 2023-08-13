"""Defines urls for driver app"""

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import DeliveryReportView

app_name = 'driver'

urlpatterns = [

    path('dashboard/', views.dashboard, name="dashboard"),
    path('support/', views.support, name="support"),
    path('raise_issue/', views.raise_issue, name="raise_issue"),
    path('messaging/', views.messaging, name="messaging"),
    path('send_message/', views.send_message, name="send_message"),
    path('reply/', views.reply, name="reply"),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('about/', views.about, name="about"),
    path('settings/', views.settings, name="settings"),
    path('notification/', views.notification, name="notification"),
    path('deliveries/', views.deliveries, name="deliveries"),
    path('accepted_delivery_details/', views.accepted_delivery_details, name="accepted_delivery_details"),
    path('delivery_details/<int:delivery_id>/', views.delivery_details, name="delivery_details"),
    path('history/', views.history, name="history"),
    path('history_details/<int:delivery_id>/', views.history_details, name='history_details'),
    path('help_documentation/', views.help_documentation, name="help_documentation"),
    path('update_actualpickupdatetime/<int:delivery_id>/', views.update_actualpickupdatetime, name='update_actualpickupdatetime'),
    path('delivery_report/<int:delivery_id>/', DeliveryReportView.as_view(), name='delivery_report'),
    path('validate_pickup_code/<int:donation_id>/', views.validate_pickup_code, name='validate_pickup_code'),
    path('logout/', views.logout_view, name='logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

