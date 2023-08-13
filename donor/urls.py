"""Defines urls for donor app"""

from django.urls import path
from . import views
from .views import DonationReportView

app_name = 'donor'

urlpatterns = [

    path('dashboard/', views.dashboard, name="dashboard"),
    path('restaurants/', views.restaurants, name="restaurants"),
    path('add_restaurant/', views.add_restaurant, name="add_restaurant"),
    path('edit_restaurant/<int:restaurant_id>/', views.edit_restaurant, name="edit_restaurant"),
    path('donate/', views.donate, name="donate"),
    path('history/', views.history, name="history"),
    path('make_donation/', views.make_donation, name="make_donation"),
    path('profile/', views.profile, name="profile"),
    path('support/', views.support, name="support"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('about/', views.about, name="about"),
    path('raise_issue/', views.raise_issue, name="raise_issue"),
    path('messaging/', views.messaging, name="messaging"),
    path('send_message/', views.send_message, name="send_message"),
    path('notification/', views.notification, name="notification"),
    path('help_documentation/', views.help_documentation, name="help_documentation"),
    path('history_details/<int:donation_id>/', views.history_details, name="history_details"),
    path('ngo_details/<int:organization_id>/', views.ngo_details, name="ngo_details"),
    path('reply/', views.reply, name="reply"),
    path('delete_restaurant/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),
    path('settings/', views.settings_view, name="settings"),
    path('donations/', views.donations, name="donations"),
    path('donation_details/<int:donation_id>/', views.donation_details, name="donation_details"),
    path('restaurant/<int:restaurant_id>/', views.restaurant_details, name='restaurant_details'),
    path('edit_donation/<int:donation_id>/', views.edit_donation, name="edit_donation"),
    path('delete_donation/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('accept_donation/<int:donation_id>/', views.accept_donation, name='accept_donation'),
    path('logout/', views.logout_view, name='logout'),
    path('my_donation_details/<int:donation_id>/', views.my_donation_details, name="my_donation_details"),
    path('perishable_donation_create/<int:donation_id>/', views.perishable_donation_create, name='perishable_donation_create'),
    path('non_perishable_donation_create/<int:donation_id>/', views.non_perishable_donation_create, name='non_perishable_donation_create'),
    path('donation_report/<int:donation_id>/', DonationReportView.as_view(), name='donation_report'),
    path('rate-organization/<int:donation_id>/', views.rate_organization, name='rate_organization'),
    path('check-rating-exists/<int:donation_id>/', views.check_rating_exists, name='check_rating_exists'),
    path('store_pickup_code/<int:donation_id>/', views.store_pickup_code, name='store_pickup_code'),
    path('send-deletion-code/', views.send_deletion_code, name='send_deletion_code'),
    path('delete-account/', views.delete_account, name='delete_account'),

]
