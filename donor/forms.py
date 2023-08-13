from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
import re
from donor.models import Restaurant, Donation, NonPerishableDonation, PerishableDonation


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


class RestaurantCreationForm(forms.ModelForm):
    Name = forms.CharField(label="Restaurant Name", max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Description = forms.CharField(label="Restaurant Description", widget=forms.Textarea(
        attrs={'class': 'form-control mb-5'}
    ))
    Photo = forms.ImageField(label="Restaurant Photo", widget=forms.ClearableFileInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Location = forms.CharField(label="Restaurant Location", max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    LicenseNumber = forms.CharField(label="Restaurant License No.", max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    HealthCertificateNumber = forms.CharField(label="Health Certificate No.", max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    def clean_name(self):
        name = self.cleaned_data['Name']
        # Add any specific name cleaning/validation if needed
        return name

    def clean_license_number(self):
        license_number = self.cleaned_data['LicenseNumber']
        # Add any specific license number cleaning/validation if needed
        return license_number

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validation if needed
        return cleaned_data

    class Meta:
        model = Restaurant
        fields = (
            'Name', 'Description', 'Photo', 'Location', 'LicenseNumber', 'HealthCertificateNumber'
        )


from django import forms
from donor.models import Restaurant, Organization


class SelectedRestaurantField(forms.ModelChoiceField):
    def label_from_instance(self, restaurant):
        return restaurant.Name  # Customize how the restaurant name is displayed in the form field


class SelectedOrganizationField(forms.ModelChoiceField):
    def label_from_instance(self, organization):
        return organization.Name  # Customize how the organization name is displayed in the form field

class DonationForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(DonationForm, self).__init__(*args, **kwargs)
        self.fields['RestaurantID'].queryset = Restaurant.objects.filter(ManagerID=user)
        self.fields['OrganizationID'].queryset = Organization.objects.all()

    RestaurantID = SelectedRestaurantField(
        queryset=Restaurant.objects.none(),
        label="Restaurant",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control appearance-none w-60 py-2.5 px-4 text-coolGray-900 text-base font-normal bg-white border outline-none border-coolGray-200 focus:border-green-500 rounded-lg shadow-input'})
    )
    OrganizationID = SelectedOrganizationField(
        queryset=Organization.objects.none(),
        label="Organization",
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
        fields = ['RestaurantID', 'OrganizationID', 'is_perishable']



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