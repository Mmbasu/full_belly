from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
import re
from donor.models import Restaurant, Donation, NonPerishableDonation, PerishableDonation
from .validators import validate_text_with_spaces_and_punctuation, validate_letters_only


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", validators=[validate_text_with_spaces_and_punctuation], required=True, max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    last_name = forms.CharField(label="Last Name", validators=[validate_text_with_spaces_and_punctuation], required=True, max_length=255, widget=forms.TextInput(
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

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError("First name should contain only letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Last name should contain only letters.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Invalid email address.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number should be numerical and contain 10 digits.")
        return phone


    def clean_twitter_link(self):
        twitter_link = self.cleaned_data.get('twitter_link')
        if twitter_link:
            if not re.match(r'^https?://(www\.)?twitter\.com/', twitter_link, re.IGNORECASE):
                raise forms.ValidationError("Invalid Twitter link.")
        return twitter_link

    def clean_instagram_link(self):
        instagram_link = self.cleaned_data.get('instagram_link')
        if instagram_link:
            if not re.match(r'^https?://(www\.)?instagram\.com/', instagram_link, re.IGNORECASE):
                raise forms.ValidationError("Invalid Instagram link.")
        return instagram_link

    def clean_facebook_link(self):
        facebook_link = self.cleaned_data.get('facebook_link')
        if facebook_link:
            if not re.match(r'^https?://(www\.)?facebook\.com/', facebook_link, re.IGNORECASE):
                raise forms.ValidationError("Invalid Facebook link.")
        return facebook_link

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError("Profile photo is required.")


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


from django import forms
from django.core.validators import validate_slug, MinLengthValidator, validate_email, MinValueValidator
from django.core.exceptions import ValidationError
from .models import Restaurant

class RestaurantCreationForm(forms.ModelForm):
    Name = forms.CharField(
        label="Restaurant Name",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[validate_text_with_spaces_and_punctuation],  # Use validate_slug to check for code injection
        error_messages={
            'required': 'This field is required.'
        },
    )

    Description = forms.CharField(
        label="Restaurant Description",
        widget=forms.Textarea(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],
        error_messages={
            'required': 'This field is required.'
        },
    )

    Photo = forms.ImageField(
        label="Restaurant Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-5'}),
    )

    Location = forms.CharField(
        label="Restaurant Location",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],  # Ensure the field is not empty
        error_messages={
            'required': 'This field is required.'
        },
    )

    LicenseNumber = forms.CharField(
        label="Restaurant License No.",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],
        error_messages={
            'required': 'This field is required.'
        },
    )

    HealthCertificateNumber = forms.CharField(
        label="Health Certificate No.",
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],  # Check for numerical value and code injection
        error_messages={
            'required': 'This field is required.'
        },
    )

    def clean(self):
        cleaned_data = super().clean()

        # Check if LicenseNumber and HealthCertificateNumber are numerical and not the same
        license_number = cleaned_data.get('LicenseNumber')
        health_certificate_number = cleaned_data.get('HealthCertificateNumber')

        if license_number is not None and not license_number.isdigit():
            raise ValidationError("License number should contain only digits.")

        if health_certificate_number is not None and not health_certificate_number.isdigit():
            raise ValidationError("Health Certificate number should contain only digits.")

        if license_number == health_certificate_number:
            raise ValidationError("License number and Health Certificate number should be different.")

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


from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


class PerishableDonationForm(forms.ModelForm):
    MealType = forms.CharField(
        label="Meal Type",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[
            MinLengthValidator(1),
            validate_text_with_spaces_and_punctuation,
            validate_letters_only,  # Use the custom validator here
        ],
        error_messages={
            'required': 'This field is required.',
        },
    )

    MealPhotos = forms.ImageField(
        label="Meal Photos",
        widget=forms.FileInput(attrs={'class': 'form-control mb-5'}),
        error_messages={
            'required': 'This field is required.',
        },
    )

    from django.core.validators import MinValueValidator

    MealQuantityPlates = forms.IntegerField(
        label="Meal Quantity (Plates)",
        widget=forms.NumberInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinValueValidator(10, 'Minimum quantity must be 10 plates')],
        error_messages={
            'required': 'This field is required.',
        },
    )

    pickup_location = forms.CharField(
        label="Pickup Location",
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation, validate_letters_only],
        error_messages={
            'required': 'This field is required.',
        },
    )

    class Meta:
        model = PerishableDonation
        fields = ['MealType', 'MealPhotos', 'MealQuantityPlates', 'pickup_location']


from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


class NonPerishableDonationForm(forms.ModelForm):
    MealTitle = forms.CharField(
        label="Meal Title",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],
        error_messages={
            'required': 'This field is required.',
        },
    )

    MealDescription = forms.CharField(
        label="Meal Description",
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],
        error_messages={
            'required': 'This field is required.',
        },
    )

    MealPhotos = forms.ImageField(
        label="Meal Photos",
        widget=forms.FileInput(attrs={'class': 'form-control mb-5'}),
        error_messages={
            'required': 'This field is required.',
        },
    )

    MealQuantityKgs = forms.DecimalField(
        label="Meal Quantity (Kgs)",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(2, 'Minimum quantity must be 2 Kgs')],
        widget=forms.NumberInput(attrs={'class': 'form-control mb-5'}),
        error_messages={
            'required': 'This field is required.',
        },
    )

    pickup_location = forms.CharField(
        label="Pickup Location",
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation, validate_letters_only],
        error_messages={
            'required': 'This field is required.',
        },
    )

    class Meta:
        model = NonPerishableDonation
        fields = ['MealTitle', 'MealDescription', 'MealPhotos', 'MealQuantityKgs', 'pickup_location']
