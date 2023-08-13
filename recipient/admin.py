from django.contrib import admin
from .models import Organization, Driver, RecipientDelivery, OrganizationRating


@admin.register(Organization)
class OrganizationModel(admin.ModelAdmin):
    list_filter = ('OrganizationID', 'Name')
    list_display = ('OrganizationID', 'Name', 'Photo', 'Location',
                    'LicenseNumber', 'ManagerID', 'Status')
    search_fields = ('Name', 'LicenseNumber')


@admin.register(Driver)
class DriverModel(admin.ModelAdmin):
    list_filter = ('DriverID', 'Status')
    list_display = ('DriverID', 'first_name', 'last_name', 'Email', 'phone', 'Username',
                    'photo', 'DriverIDNumber', 'DrivingLicenseNumber', 'CarNumberPlate', 'OrganizationID', 'Status')
    search_fields = ('DriverIDNumber', 'CarNumberPlate')


@admin.register(RecipientDelivery)
class RecipientDeliveryModel(admin.ModelAdmin):
    list_filter = ('DeliveryID',)
    list_display = ('DeliveryID', 'DonationID', 'DriverID',
                    'Status', 'PickupDateTime')
    search_fields = ('Status',)


@admin.register(OrganizationRating)
class RatingModel(admin.ModelAdmin):
    list_filter = ('rating',)
    list_display = ('user', 'restaurant', 'rating', 'organization', 'donation', 'rated_entity_type')
