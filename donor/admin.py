from django.contrib import admin
from .models import Restaurant, Donation, PerishableDonation, NonPerishableDonation, RestaurantRating


# Register your models here.

@admin.register(Restaurant)
class RestaurantModel(admin.ModelAdmin):
    list_filter = ('RestaurantID', 'Name')
    list_display = ('RestaurantID', 'Name', 'Photo', 'Location', 'Status',
                    'LicenseNumber', 'HealthCertificateNumber', 'ManagerID')
    search_fields = ('Name', 'LicenseNumber')

@admin.register(RestaurantRating)
class RatingModel(admin.ModelAdmin):
    list_filter = ('rating',)
    list_display = ('user', 'restaurant', 'rating', 'organization', 'donation', 'rated_entity_type')

@admin.register(Donation)
class DonationModel(admin.ModelAdmin):
    list_filter = ('DonationID',)
    list_display = ('DonationID', 'RestaurantID', 'is_perishable', 'driver', 'date_delivered', 'accepted_timestamp', 'pickup_code',
                    'Organization', 'is_accepted', 'ngo_requested', 'Status', 'is_scheduled', 'date_posted', 'pickup_time')
    search_fields = ('is_perishable', 'is_accepted')


@admin.register(PerishableDonation)
class PerishableDonationModel(admin.ModelAdmin):
    list_filter = ('Donation',)
    list_display = ('Donation', 'MealType', 'MealPhotos', 'created_at',
                    'MealQuantityPlates', 'pickup_location')
    search_fields = ('Donation', 'MealType')


@admin.register(NonPerishableDonation)
class NonPerishableDonationModel(admin.ModelAdmin):
    list_filter = ('Donation',)
    list_display = ('Donation', 'MealTitle', 'MealDescription', 'MealPhotos',
                    'MealQuantityKgs', 'pickup_location')
    search_fields = ('Donation', 'MealTitle')
