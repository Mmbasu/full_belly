from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.utils import timezone

from recipient.models import Organization, Driver


def default_restaurant_photo():
    return 'restaurant_photos/default_restaurant_photo.png'


class Restaurant(models.Model):
    STATUS_CHOICES = (
        ('Unverified', 'Unverified'),
        ('Verified', 'Verified'),
    )

    RestaurantID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Photo = models.ImageField(upload_to='restaurant_photos/', default=default_restaurant_photo)
    Location = models.CharField(max_length=255)
    LicenseNumber = models.CharField(max_length=255)
    HealthCertificateNumber = models.CharField(max_length=255)
    ManagerID = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'donor'},
    )
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unverified')

    def __str__(self):
        return self.Name

    def average_rating(self):
        return self.restaurantrating.aggregate(Avg('rating'))['rating__avg']

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'


class Donation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('Intransit', 'Intransit'),
    )

    DonationID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='donations')
    Organization = models.ForeignKey('recipient.Organization', on_delete=models.CASCADE)
    is_perishable = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=False)
    ngo_requested = models.BooleanField(default=False)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date_posted = models.DateTimeField(default=timezone.now)
    pickup_time = models.DateTimeField(default=timezone.now, blank=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    date_delivered = models.DateTimeField(null=True, blank=True)
    accepted_timestamp = models.DateTimeField(null=True, blank=True)
    pickup_code = models.CharField(max_length=5, default='19456')

    def __str__(self):
        return f"Donation {self.DonationID} from {self.RestaurantID} to {self.Organization}"

    def accept_donation(self):
        self.is_accepted = True
        self.accepted_timestamp = timezone.now()
        self.save()


    class Meta:
        verbose_name = 'donation'
        verbose_name_plural = 'donations'



class PerishableDonationManager(models.Manager):
    def delete_expired_meals(self):
        expired_meals = self.filter(meal_expiry_time__lt=timezone.now())
        expired_meals.delete()


def default_perishable_meal_photo():
    return 'meal_photos_perishable/default_perishable_meal.jpg'


class PerishableDonation(models.Model):
    Donation = models.OneToOneField(Donation, on_delete=models.CASCADE, primary_key=True)
    MealType = models.CharField(max_length=255)
    MealPhotos = models.ImageField(upload_to='meal_photos_perishable/', default=default_perishable_meal_photo)
    MealQuantityPlates = models.PositiveIntegerField()
    pickup_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PerishableDonationManager()

    def __str__(self):
        return f"Perishable Donation from {self.Donation.RestaurantID} to {self.Donation.Organization}"

    class Meta:
        verbose_name = 'perishable donation'
        verbose_name_plural = 'perishable donations'


def default_nonperishable_meal_photo():
    return 'meal_photos_non_perishable/default_nonperishable_meal.jpeg'


class NonPerishableDonation(models.Model):
    Donation = models.OneToOneField(Donation, on_delete=models.CASCADE, primary_key=True)
    MealTitle = models.CharField(max_length=255)
    MealDescription = models.TextField()
    MealPhotos = models.ImageField(upload_to='meal_photos_non_perishable/', default=default_nonperishable_meal_photo)
    MealQuantityKgs = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    pickup_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Non-Perishable Donation from {self.Donation.RestaurantID} to {self.Donation.Organization}"

    class Meta:
        verbose_name = 'non-perishable donation'
        verbose_name_plural = 'non-perishable donations'




from django.conf import settings

class RestaurantRating(models.Model):
    RATING_CHOICES = [
        ('RESTAURANT', 'Restaurant'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('donor.Restaurant', on_delete=models.CASCADE, null=True, blank=True, related_name='restaurantrating')
    organization = models.ForeignKey('recipient.Organization', on_delete=models.CASCADE, null=True, blank=True)
    donation = models.ForeignKey('donor.Donation', on_delete=models.CASCADE, null=True, blank=True)
    rated_entity_type = models.CharField(max_length=20, choices=RATING_CHOICES)
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(5.0)])

    def __str__(self):
        if self.rated_entity_type == 'RESTAURANT':
            return f"Rating {self.rating} for Restaurant {self.restaurant}"
        else:
            return f"Invalid Rating Entity Type"
