from django.contrib import admin
from .models import Organization, Driver, RecipientDelivery


@admin.register(Organization)
class OrganizationModel(admin.ModelAdmin):
    list_filter = ('OrganizationID', 'Name')
    list_display = ('OrganizationID', 'Name', 'Photo', 'Location',
                    'LicenseNumber', 'ManagerID')
    search_fields = ('Name', 'LicenseNumber')


@admin.register(Driver)
class DriverModel(admin.ModelAdmin):
    list_filter = ('DriverID', 'Status')
    list_display = ('DriverID', 'first_name', 'last_name', 'Email', 'Phone', 'Username',
                    'Photo', 'DriverIDNumber', 'DrivingLicenseNumber', 'CarNumberPlate', 'OrganizationID', 'Status')
    search_fields = ('DriverIDNumber', 'CarNumberPlate')


@admin.register(RecipientDelivery)
class RecipientDeliveryModel(admin.ModelAdmin):
    list_filter = ('DeliveryID',)
    list_display = ('DeliveryID', 'DonationID', 'DriverID',
                    'Status', 'PickupDateTime', 'Destination')
    search_fields = ('Status', 'Destination')

