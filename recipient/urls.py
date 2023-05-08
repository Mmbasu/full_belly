"""Defines urls for recipient app"""

from django.urls import path
from . import views

app_name = 'recipient'

urlpatterns = [

    path('dashboard/', views.dashboard, name="dashboard"),
    path('history/', views.history, name="history"),
    path('profile/', views.profile, name="profile"),
    path('support/', views.support, name="support"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('about/', views.about, name="about"),
    path('raise_issue/', views.raise_issue, name="raise_issue"),
    path('messaging/', views.messaging, name="messaging"),
    path('send_message/', views.send_message, name="send_message"),
    path('notification/', views.notification, name="notification"),
    path('help_documentation/', views.help_documentation, name="help_documentation"),
    path('history_details/', views.history_details, name="history_details"),
    path('reply/', views.reply, name="reply"),
    path('settings/', views.settings, name="settings"),
    path('donation/', views.donation, name="donation"),
    path('request_donation_1/', views.request_donation_1, name="request_donation_1"),
    path('request_donation/', views.request_donation, name="request_donation"),
    path('donation_details/', views.donation_details, name="donation_details"),
    path('edit_donation_request/', views.edit_donation_request, name="edit_donation_request"),
    path('accepted_donation_details/', views.accepted_donation_details, name="accepted_donation_details"),
    path('restaurant_details/', views.restaurant_details, name="restaurant_details"),
    path('ngo_details/', views.ngo_details, name="ngo_details"),
    path('edit_ngo_details/', views.edit_ngo_details, name="edit_ngo_details"),
    path('drivers/', views.drivers, name="drivers"),
    path('edit_driver/', views.edit_driver, name="edit_driver"),
    path('driver_details/', views.driver_details, name="driver_details"),
    path('add_driver/', views.add_driver, name="add_driver"),

]
