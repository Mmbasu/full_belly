from django.contrib.auth import get_user_model
from django.db import models
from users.models import CustomUser, CustomUserManager


class Organization(models.Model):
    OrganizationID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Photo = models.ImageField(upload_to='organization_photos/')
    Location = models.CharField(max_length=255, unique=True)
    LicenseNumber = models.CharField(max_length=255)
    ManagerID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'organization'
        verbose_name_plural = 'organizations'


class Driver(models.Model):
    STATUS_CHOICES = (
        ('idle', 'idle'),
        ('onDelivery', 'onDelivery'),
        ('off-Work', 'off-Work'),
    )

    DriverID = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='driver'
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    Username = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='idle')
    Phone = models.CharField(max_length=255)
    Photo = models.ImageField(upload_to='driver_photos/')
    DriverIDNumber = models.CharField(max_length=255)
    DrivingLicenseNumber = models.CharField(max_length=255)
    CarNumberPlate = models.CharField(max_length=255)
    OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)

    USERNAME_FIELD = 'Username'  # Specify the username field
    REQUIRED_FIELDS = ['Email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        # Set the password for the associated CustomUser
        self.DriverID.set_password(raw_password)

    def get_username(self):
        return self.Username

    def get_email(self):
        return self.Email

    # Implement other required methods and attributes for authentication
    # ...

    class Meta:
        verbose_name = 'driver'
        verbose_name_plural = 'drivers'


class RecipientDelivery(models.Model):
    STATUS_CHOICES = (
        ('future', 'future'),
        ('delivered', 'delivered'),
        ('intransit', 'intransit'),
    )

    DonationID = models.ForeignKey('donor.Donation', on_delete=models.CASCADE)
    DriverID = models.ForeignKey(Driver, on_delete=models.CASCADE)
    DeliveryID = models.OneToOneField('driver.Delivery', on_delete=models.CASCADE, primary_key=True)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='future')
    PickupDateTime = models.DateTimeField()
    Destination = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        to_field='Location',
        limit_choices_to={'Location__isnull': False},
    )

    def __str__(self):
        return f"Delivery {self.DeliveryID} (Recipient View)"

    class Meta:
        verbose_name = 'recipient delivery'
        verbose_name_plural = 'recipient deliveries'
