import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from donor.models import NonPerishableDonation, PerishableDonation, Donation, Restaurant
from users.models import CustomUser
from .models import Driver, Organization


class DriverCreationForm(UserCreationForm):
    Email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Username = forms.CharField(label="Username", required=True, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    first_name = forms.CharField(label="First Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    last_name = forms.CharField(label="Last Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    phone = forms.CharField(label="phone", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    photo = forms.ImageField(label="photo", widget=forms.ClearableFileInput(
        attrs={'class': 'form-control mb-5'}
    ))

    DriverIDNumber = forms.CharField(label="Driver ID Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    DrivingLicenseNumber = forms.CharField(label="Driving License Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    CarNumberPlate = forms.CharField(label="Car Number Plate", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5'}
    ))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5'}
    ))

    def clean_email(self):
        email = self.cleaned_data['Email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    class Meta:
        model = Driver
        fields = (
            'first_name', 'last_name', 'Email', 'Username', 'phone', 'photo', 'DriverIDNumber', 'DrivingLicenseNumber',
            'CarNumberPlate', 'password1', 'password2'
        )


class OrganizationForm(forms.ModelForm):
    Name = forms.CharField(label="NGO Name", required=True, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Description = forms.CharField(label="NGO Description", required=True, widget=forms.Textarea(
        attrs={'class': 'form-control mb-5', 'rows': 5}
    ))
    Photo = forms.ImageField(label="NGO Photo", required=True, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Location = forms.CharField(label="NGO Location", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    LicenseNumber = forms.CharField(label="NGO License No.", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    class Meta:
        model = Organization
        fields = ['Name', 'Description', 'Photo', 'Location', 'LicenseNumber']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('Name')
        description = cleaned_data.get('Description')
        location = cleaned_data.get('Location')
        license_number = cleaned_data.get('LicenseNumber')

        if not name or not description or not location or not license_number:
            raise forms.ValidationError("All fields are required.")

        return cleaned_data


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", required=True, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    last_name = forms.CharField(label="Last Name", required=True, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control mb-5'}
    ))
    phone = forms.CharField(label="phone", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    photo = forms.ImageField(label="photo", required=True, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control mb-5'}
    ))
    twitter_link = forms.URLField(label="Twitter Link", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    instagram_link = forms.URLField(label="Instagram Link", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    facebook_link = forms.URLField(label="Facebook Link", required=False, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'phone', 'photo', 'twitter_link', 'instagram_link',
                  'facebook_link']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')

        if not first_name or not last_name or not email or not phone:
            raise forms.ValidationError("All fields are required.")

        return cleaned_data

    def clean_twitter_link(self):
        twitter_link = self.cleaned_data.get('twitter_link')
        if twitter_link:
            if not re.match(r'^https?://(www\.)?twitter\.com/', twitter_link):
                raise forms.ValidationError("Invalid Twitter link.")
        else:
            twitter_link = self.instance.twitter_link  # Use existing value
        return twitter_link

    def clean_instagram_link(self):
        instagram_link = self.cleaned_data.get('instagram_link')
        if instagram_link:
            if not re.match(r'^https?://(www\.)?instagram\.com/', instagram_link):
                raise forms.ValidationError("Invalid Instagram link.")
        else:
            instagram_link = self.instance.instagram_link  # Use existing value
        return instagram_link

    def clean_facebook_link(self):
        facebook_link = self.cleaned_data.get('facebook_link')
        if facebook_link:
            if not re.match(r'^https?://(www\.)?facebook\.com/', facebook_link):
                raise forms.ValidationError("Invalid Facebook link.")
        else:
            facebook_link = self.instance.facebook_link  # Use existing value
        return facebook_link

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError("Profile photo is required.")

        # Add additional validation for the profile photo if needed

        return photo


class DriverUpdateForm(forms.ModelForm):
    Email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Username = forms.CharField(label="Username", required=True, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    first_name = forms.CharField(label="First Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    last_name = forms.CharField(label="Last Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    phone = forms.CharField(label="phone", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    photo = forms.ImageField(label="photo", required=False, widget=forms.FileInput(
        attrs={'class': 'form-control mb-5'}
    ))

    DriverIDNumber = forms.CharField(label="Driver ID Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    DrivingLicenseNumber = forms.CharField(label="Driving License Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    CarNumberPlate = forms.CharField(label="Car Number Plate", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    class Meta:
        model = Driver
        fields = (
            'first_name', 'last_name', 'Email', 'Username', 'phone', 'photo',
            'DriverIDNumber', 'DrivingLicenseNumber', 'CarNumberPlate',
        )


from django import forms
from donor.models import Restaurant

class SelectedRestaurantField(forms.ModelChoiceField):
    def label_from_instance(self, restaurant):
        return restaurant.Name  # Customize how the restaurant name is displayed in the form field




class DonationForm(forms.ModelForm):
    RestaurantID = SelectedRestaurantField(
        queryset=Restaurant.objects.all(),
        label="Restaurant",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control appearance-none w-60 py-2.5 px-4 text-coolGray-900 text-base font-normal bg-white border outline-none border-coolGray-200 focus:border-green-500 rounded-lg shadow-input'})
    )
    is_perishable = forms.BooleanField(
        label="Is Perishable",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input border outline-none border-coolGray-200 focus:border-green-500 rounded-sm'})
    )

    class Meta:
        model = Donation
        fields = ['RestaurantID', 'is_perishable']



class PerishableDonationForm(forms.ModelForm):
    MealType = forms.CharField(
        label="Meal Type",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'})
    )
    MealPhotos = forms.ImageField(
        label="Meal Photos",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control mb-5'})
    )
    MealQuantityPlates = forms.IntegerField(
        label="Meal Quantity (Plates)",
        widget=forms.NumberInput(attrs={'class': 'form-control mb-5'})
    )
    pickup_location = forms.CharField(
        label="Pickup Location",
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'})
    )

    class Meta:
        model = PerishableDonation
        fields = ['MealType', 'MealPhotos', 'MealQuantityPlates', 'pickup_location']


class NonPerishableDonationForm(forms.ModelForm):
    MealTitle = forms.CharField(
        label="Meal Title",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'})
    )
    MealDescription = forms.CharField(
        label="Meal Description",
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'})
    )
    MealPhotos = forms.ImageField(
        label="Meal Photos",
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control mb-5'})
    )
    MealQuantityKgs = forms.DecimalField(
        label="Meal Quantity (Kgs)",
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control mb-5'})
    )
    pickup_location = forms.CharField(
        label="Pickup Location",
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'})
    )

    class Meta:
        model = NonPerishableDonation
        fields = ['MealTitle', 'MealDescription', 'MealPhotos', 'MealQuantityKgs', 'pickup_location']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-80 px-4 py-2.5 text-base text-coolGray-900 font-normal outline-none focus:border-green-500 border border-coolGray-200 rounded-lg shadow-input',
            'required': 'required',
            'placeholder': '********'
        }),

    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-80 px-4 py-2.5 text-base text-coolGray-900 font-normal outline-none focus:border-green-500 border border-coolGray-200 rounded-lg shadow-input',
            'required': 'required',
            'placeholder': '********'
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-80 px-4 py-2.5 text-base text-coolGray-900 font-normal outline-none focus:border-green-500 border border-coolGray-200 rounded-lg shadow-input',
            'required': 'required',
            'placeholder': '********'
        }),
    )
