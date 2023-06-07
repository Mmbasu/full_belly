from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        username = extra_fields.pop('username', email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('recipient', 'Recipient'),
        ('driver', 'Driver'),
    )

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=True)
    activation_token = models.CharField(max_length=40, blank=True, null=True)
    password_reset_token = models.CharField(max_length=40, blank=True, null=True)
    password_reset_token_created_at = models.DateTimeField(blank=True, null=True)
    password_reset_used = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def generate_password_reset_token(self):
        token = default_token_generator.make_token(self)
        self.password_reset_token = token
        self.password_reset_token_created_at = timezone.now()
        self.save()
        return token

    def mark_password_reset_token_used(self):
        self.password_reset_used = True
        self.save()

    def is_password_reset_token_valid(self, token):
        if self.password_reset_token is None:
            return False
        return default_token_generator.check_token(self, token)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

