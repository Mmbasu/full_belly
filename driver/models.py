from django.db import models
from geopy.distance import geodesic
from datetime import datetime


class Delivery(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('delivered', 'delivered'),
        ('Intransit', 'Intransit'),
    )

    DonationID = models.ForeignKey('donor.Donation', on_delete=models.CASCADE)
    DeliveryID = models.OneToOneField('recipient.RecipientDelivery', on_delete=models.CASCADE, primary_key=True)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    PickupDateTime = models.DateTimeField()
    PickupPoint = models.CharField(max_length=255)
    DriverID = models.ForeignKey('recipient.Driver', on_delete=models.CASCADE)
    DistanceTraveled = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TimeSpentOnRoad = models.DurationField(null=True, blank=True)
    ActualPickupDateTime = models.DateTimeField(null=True, blank=True)

    @property
    def distance_traveled(self):
        pickup_location = self.DonationID.RestaurantID.Location
        destination_location = self.Destination
        distance = geodesic(pickup_location, destination_location).kilometers
        return distance

    @property
    def time_spent_on_road(self):
        pickup_time = self.ActualPickupDateTime
        delivered_time = self.DonationID.date_delivered

        if pickup_time and delivered_time:
            time_spent = delivered_time - pickup_time
            return time_spent

        return None

    @classmethod
    def get_deliveries_made(cls):
        return cls.objects.filter(Status='delivered').count()

    def __str__(self):
        return f"Delivery {self.DeliveryID}"

    class Meta:
        verbose_name = 'delivery'
        verbose_name_plural = 'deliveries'

