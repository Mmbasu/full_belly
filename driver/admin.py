from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryModel(admin.ModelAdmin):
    list_filter = ('DeliveryID',)
    list_display = ('DeliveryID', 'DonationID', 'DriverID', 'AcceptedDelivery', 'PickupCode',
                    'Status', 'PickupDateTime', 'Destination')
    search_fields = ('Status', 'Destination')
