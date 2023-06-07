from django.contrib import admin
from .models import Restaurant, Donation, PerishableDonation, NonPerishableDonation


# Register your models here.

@admin.register(Restaurant)
class RestaurantModel(admin.ModelAdmin):
    list_filter = ('RestaurantID', 'Name')
    list_display = ('RestaurantID', 'Name', 'Photo', 'Location',
                    'LicenseNumber', 'HealthCertificateNumber', 'ManagerID')
    search_fields = ('Name', 'LicenseNumber')


@admin.register(Donation)
class DonationModel(admin.ModelAdmin):
    list_filter = ('DonationID',)
    list_display = ('DonationID', 'RestaurantID', 'is_perishable',
                    'Organization', 'PickupTime')
    search_fields = ('is_perishable',)


@admin.register(PerishableDonation)
class PerishableDonationModel(admin.ModelAdmin):
    list_filter = ('Donation',)
    list_display = ('Donation', 'MealType', 'MealPhotos', 'created_at',
                    'MealQuantityPlates', 'meal_expiry_time', 'pickup_location')
    search_fields = ('Donation', 'MealType')


@admin.register(NonPerishableDonation)
class NonPerishableDonationModel(admin.ModelAdmin):
    list_filter = ('Donation',)
    list_display = ('Donation', 'MealTitle', 'MealDescription', 'MealPhotos',
                    'MealQuantityKgs', 'pickup_location')
    search_fields = ('Donation', 'MealTitle')
