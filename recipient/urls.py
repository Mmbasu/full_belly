"""Defines urls for recipient app"""

from django.urls import path

from .views import DonationReportView
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import delete_driver, MarkAsDeliveredView

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
                  path('settings/', views.settings_view, name="settings"),
                  path('donation/', views.donation, name="donation"),
                    path('donation_details/<int:donation_id>/', views.donation_details, name="donation_details"),
                  path('request_donation_1/', views.request_donation_1, name="request_donation_1"),
                  path('request_donation/', views.request_donation, name="request_donation"),
                  path('history_details/<int:donation_id>/', views.history_details, name="history_details"),
                  path('edit_donation_request/<int:donation_id>/', views.edit_donation_request, name="edit_donation_request"),
                  path('accepted_donation_details/<int:donation_id>/', views.accepted_donation_details, name="accepted_donation_details"),
                  path('restaurant_details/<int:restaurant_id>/', views.restaurant_details, name="restaurant_details"),
                  path('ngo_details/', views.ngo_details, name="ngo_details"),
                  path('edit_ngo_details/', views.edit_ngo_details, name="edit_ngo_details"),
                  path('drivers/', views.driver_list, name="drivers"),
                  path('edit_driver/<int:driver_id>/', views.edit_driver, name='edit_driver'),
                  path('driver_details/<int:driver_id>/', views.driver_details, name='driver_details'),
                  path('add_driver/', views.add_driver, name="add_driver"),
                  path('delete-driver/<int:driver_id>/', views.delete_driver, name='delete_driver'),
                  path('logout/', views.logout_view, name='logout'),
                    path('accept_donation/<int:donation_id>/', views.accept_donation, name='accept_donation'),
                  path('get_ngos_drivers/', views.get_ngos_drivers, name='get_ngos_drivers'),
                  path('save_schedule_pickup/', views.save_schedule_pickup, name='save_schedule_pickup'),
                    path('delete_donation/<int:donation_id>/', views.delete_donation, name='delete_donation'),
                    path('perishable_donation_create/<int:donation_id>/', views.perishable_donation_create, name='perishable_donation_create'),
                    path('non_perishable_donation_create/<int:donation_id>/', views.non_perishable_donation_create, name='non_perishable_donation_create'),
                    path('donation/mark_as_delivered/<int:donation_id>/', MarkAsDeliveredView.as_view(), name='mark_as_delivered'),
                    path('donation_report/<int:donation_id>/', DonationReportView.as_view(), name='donation_report'),
                    path('rate-restaurant/<int:donation_id>/', views.rate_restaurant, name='rate_restaurant'),
                    path('check-rating-exists/<int:donation_id>/', views.check_rating_exists, name='check_rating_exists'),
                    path('send-deletion-code/', views.send_deletion_code, name='send_deletion_code'),
                    path('delete-account/', views.delete_account, name='delete_account'),
                    path('check-password/', views.check_password_view, name='check_password'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
