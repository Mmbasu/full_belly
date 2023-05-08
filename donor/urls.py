"""Defines urls for donor app"""

from django.urls import path
from . import views

app_name = 'donor'

urlpatterns = [

    path('dashboard/', views.dashboard, name="dashboard"),
    path('restaurants/', views.restaurants, name="restaurants"),
    path('add_restaurant/', views.add_restaurant, name="add_restaurant"),
    path('edit_restaurant/', views.edit_restaurant, name="edit_restaurant"),
    path('donate/', views.donate, name="donate"),
    path('history/', views.history, name="history"),
    path('make_donation/', views.make_donation, name="make_donation"),
    path('profile/', views.profile, name="profile"),
    path('support/', views.support, name="support"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('about/', views.about, name="about"),
    path('raise_issue/', views.raise_issue, name="raise_issue"),
    path('messaging/', views.messaging, name="messaging"),
    path('send_message/', views.send_message, name="send_message"),
    path('notification/', views.notification, name="notification"),
    path('help_documentation/', views.help_documentation, name="help_documentation"),
    path('history_details/', views.history_details, name="history_details"),
    path('ngo_details/', views.ngo_details, name="ngo_details"),
    path('reply/', views.reply, name="reply"),
    path('settings/', views.settings, name="settings"),
    path('donations/', views.donations, name="donations"),
    path('donation_details/', views.donation_details, name="donation_details"),
    path('edit_donation/', views.edit_donation, name="edit_donation"),
    path('my_donation_details/', views.my_donation_details, name="my_donation_details"),

]
