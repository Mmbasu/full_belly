from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import CustomUser, CustomUserManager


def default_ngo_photo():
    return 'organization_photos/ngo_default.jpg'


class Organization(models.Model):
    STATUS_CHOICES = (
        ('Unverified', 'Unverified'),
        ('Verified', 'Verified'),
    )

    OrganizationID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Photo = models.ImageField(upload_to='organization_photos/', default=default_ngo_photo)
    Location = models.CharField(max_length=255, unique=True)
    LicenseNumber = models.CharField(max_length=255)
    ManagerID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unverified')

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = 'organization'
        verbose_name_plural = 'organizations'


class Driver(models.Model):
    STATUS_CHOICES = (
        ('idle', 'idle'),
        ('onDelivery', 'onDelivery'),
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
    phone = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='driver_photos/')
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
        ('pending', 'pending'),
        ('delivered', 'delivered'),
        ('Intransit', 'Intransit'),
    )

    DeliveryID = models.AutoField(primary_key=True)
    ManagerID = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipient')
    DonationID = models.ForeignKey('donor.Donation', on_delete=models.CASCADE)
    DriverID = models.ForeignKey(Driver, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    PickupDateTime = models.DateTimeField()

    def __str__(self):
        return f"Delivery {self.DeliveryID}"

    class Meta:
        verbose_name = 'recipient delivery'
        verbose_name_plural = 'recipient deliveries'

class OrganizationRating(models.Model):
    RATING_CHOICES = [
        ('ORGANIZATION', 'Organization'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('donor.Restaurant', on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey('recipient.Organization', on_delete=models.CASCADE, null=True, blank=True, related_name='organizationrating')
    donation = models.ForeignKey('donor.Donation', on_delete=models.CASCADE, null=True, blank=True)
    rated_entity_type = models.CharField(max_length=20, choices=RATING_CHOICES)
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(5.0)])

    def __str__(self):
        if self.rated_entity_type == 'ORGANIZATION':
            return f"Rating {self.rating} for ORGANIZATION {self.restaurant}"
        else:
            return f"Invalid Rating Entity Type"
