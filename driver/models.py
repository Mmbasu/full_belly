from django.db import models
from geopy.distance import geodesic
from datetime import datetime


class Delivery(models.Model):
    STATUS_CHOICES = (
        ('future', 'future'),
        ('delivered', 'delivered'),
        ('intransit', 'intransit'),
    )

    DeliveryID = models.AutoField(primary_key=True)
    DonationID = models.ForeignKey('donor.Donation', on_delete=models.CASCADE)
    PickupCode = models.CharField(max_length=5, default='00000')
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='future')
    PickupDateTime = models.DateTimeField()
    Destination = models.CharField(max_length=255)
    DriverID = models.ForeignKey('recipient.Driver', on_delete=models.CASCADE)
    AcceptedDelivery = models.BooleanField(default=False)
    DistanceTraveled = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TimeSpentOnRoad = models.DurationField(null=True, blank=True)

    @property
    def distance_traveled(self):
        pickup_location = self.DonationID.RestaurantID.Location
        destination_location = self.Destination
        distance = geodesic(pickup_location, destination_location).kilometers
        return distance

    @property
    def time_spent_on_road(self):
        pickup_time = self.PickupDateTime
        current_time = datetime.now()
        time_spent = current_time - pickup_time
        return time_spent

    @classmethod
    def get_deliveries_made(cls):
        return cls.objects.filter(Status='delivered').count()

    def __str__(self):
        return f"Delivery {self.DeliveryID}"

    class Meta:
        verbose_name = 'delivery'
        verbose_name_plural = 'deliveries'

