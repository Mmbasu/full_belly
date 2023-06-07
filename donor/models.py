from django.core.validators import MinValueValidator
from django.db import models
from users.models import CustomUser


class Restaurant(models.Model):
    RestaurantID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Photo = models.ImageField(upload_to='restaurant_photos/')
    Location = models.CharField(max_length=255)
    LicenseNumber = models.CharField(max_length=255)
    HealthCertificateNumber = models.CharField(max_length=255)
    ManagerID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'restaurant'
        verbose_name_plural = 'restaurants'


class Donation(models.Model):
    DonationID = models.AutoField(primary_key=True)
    RestaurantID = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    Organization = models.ForeignKey('recipient.Organization', on_delete=models.CASCADE)
    is_perishable = models.BooleanField()
    PickupTime = models.DateTimeField()

    def __str__(self):
        return f"Donation from {self.RestaurantID} to {self.Organization}"

    class Meta:
        verbose_name = 'donation'
        verbose_name_plural = 'donations'

class PerishableDonationManager(models.Manager):
    def delete_expired_meals(self):
        expired_meals = self.filter(meal_expiry_time__lt=timezone.now())
        expired_meals.delete()

class PerishableDonation(models.Model):
    Donation = models.OneToOneField(Donation, on_delete=models.CASCADE, primary_key=True)
    MealType = models.CharField(max_length=255)
    MealPhotos = models.ImageField(upload_to='meal_photos_perishable/')
    MealQuantityPlates = models.PositiveIntegerField()
    meal_expiry_time = models.TimeField
    pickup_location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PerishableDonationManager()

    def __str__(self):
        return f"Perishable Donation from {self.Donation.RestaurantID} to {self.Donation.Organization}"

    class Meta:
        verbose_name = 'perishable donation'
        verbose_name_plural = 'perishable donations'




class NonPerishableDonation(models.Model):
    Donation = models.OneToOneField(Donation, on_delete=models.CASCADE, primary_key=True)
    MealTitle = models.CharField(max_length=255)
    MealDescription = models.TextField()
    MealPhotos = models.ImageField(upload_to='meal_photos_non_perishable/')
    MealQuantityKgs = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    pickup_location = models.CharField(max_length=255)

    def __str__(self):
        return f"Non-Perishable Donation from {self.Donation.RestaurantID} to {self.Donation.Organizaton}"

    class Meta:
        verbose_name = 'non-perishable donation'
        verbose_name_plural = 'non-perishable donations'