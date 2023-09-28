import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.validators import validate_email, MinValueValidator, MinLengthValidator

from donor.models import NonPerishableDonation, PerishableDonation, Donation, Restaurant
from donor.validators import validate_text_with_spaces_and_punctuation, validate_letters_only
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

    DriverIDNumber = forms.CharField(label="Driver ID Number", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    DrivingLicenseNumber = forms.CharField(label="Driving License Number", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    CarNumberPlate = forms.CharField(label="Car Number Plate", max_length=8, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5', 'required': 'required'}
    ))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5', 'required': 'required'}
    ))

    def clean_DriverIDNumber(self):
        driver_id_number = self.cleaned_data['DriverIDNumber']
        if not driver_id_number.isdigit():
            raise forms.ValidationError("Driver ID Number should only contain numbers")
        return driver_id_number

    import re

    def clean_DrivingLicenseNumber(self):
        license_number = self.cleaned_data['DrivingLicenseNumber']
        # Use a regular expression to match the desired format
        if not re.match(r'^DL-\d{7}$', license_number):
            raise forms.ValidationError(
                "Driving License Number should be in the format 'DL-1234567'")

        return license_number

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
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
            return email
        except forms.ValidationError:
            raise forms.ValidationError("Invalid email address.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number should be numerical and contain 10 digits only.")
        return phone

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError("Profile photo is required.")

        return photo

    class Meta:
        model = Driver
        fields = (
            'first_name', 'last_name', 'Email', 'Username', 'phone', 'photo', 'DriverIDNumber', 'DrivingLicenseNumber',
            'CarNumberPlate', 'password1', 'password2'
        )


from django import forms
from .models import Organization


class OrganizationForm(forms.ModelForm):
    Name = forms.CharField(
        label="NGO Name",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[validate_text_with_spaces_and_punctuation, validate_letters_only],
        # Use validate_slug to check for code injection
        error_messages={
            'required': 'This field is required.'
        },
    )
    Description = forms.CharField(
        label="NGO Description",
        widget=forms.Textarea(attrs={'class': 'form-control mb-5', 'rows': 5}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation],
        error_messages={
            'required': 'This field is required.'
        },
    )
    Photo = forms.ImageField(label="NGO Photo", required=True, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Location = forms.CharField(
        label="NGO Location",
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

    class Meta:
        model = Organization
        fields = ['Name', 'Description', 'Photo', 'Location', 'LicenseNumber']

    def clean_photo(self):
        photo = self.cleaned_data.get('Photo')

        if not photo:
            raise forms.ValidationError("Profile photo is required.")

        return photo

    def clean_LicenseNumber(self):
        LicenseNumber = self.cleaned_data.get('LicenseNumber')
        if not LicenseNumber.isdigit():
            raise forms.ValidationError("The License Number should only contain numbers.")
        return LicenseNumber


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", validators=[validate_text_with_spaces_and_punctuation],
                                 required=True, max_length=255, widget=forms.TextInput(
            attrs={'class': 'form-control mb-5'}
        ))
    last_name = forms.CharField(label="Last Name", validators=[validate_text_with_spaces_and_punctuation],
                                required=True, max_length=255, widget=forms.TextInput(
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
            raise forms.ValidationError("Phone number should be numerical and contain 10 digits")
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


class DriverUpdateForm(forms.ModelForm):
    Email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    Username = forms.CharField(label="Username", validators=[validate_text_with_spaces_and_punctuation], required=True,
                               max_length=30, widget=forms.TextInput(
            attrs={'class': 'form-control mb-5'}
        ))
    first_name = forms.CharField(label="First Name", max_length=30,
                                 validators=[validate_text_with_spaces_and_punctuation], required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control mb-5'}
                                 ))
    last_name = forms.CharField(label="Last Name", max_length=30,
                                validators=[validate_text_with_spaces_and_punctuation], required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control mb-5'}
                                ))
    phone = forms.CharField(label="phone", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    photo = forms.ImageField(label="photo", required=False, widget=forms.FileInput(
        attrs={'class': 'form-control mb-5'}
    ))

    DriverIDNumber = forms.CharField(label="Driver ID Number", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    DrivingLicenseNumber = forms.CharField(label="Driving License Number", max_length=15, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    ))
    CarNumberPlate = forms.CharField(label="Car Number Plate", max_length=8,
                                     validators=[validate_text_with_spaces_and_punctuation], widget=forms.TextInput(
            attrs={'class': 'form-control mb-5'}
        ))

    def clean_DriverIDNumber(self):
        driver_id_number = self.cleaned_data['DriverIDNumber']
        if not driver_id_number.isdigit():
            raise forms.ValidationError("Driver ID Number should only contain numbers.")
        return driver_id_number

    def clean_DrivingLicenseNumber(self):
        license_number = self.cleaned_data['DrivingLicenseNumber']
        # Use a regular expression to match the desired format
        if not re.match(r'^DL-\d{7}$', license_number):
            raise forms.ValidationError(
                "Driving License Number should be in the format 'DL-1234567'")

        return license_number

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
            raise forms.ValidationError("Phone number should be numerical and contain 10 digits only.")
        return phone

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if not photo:
            raise forms.ValidationError("Profile photo is required.")

        return photo

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
        widget=forms.Select(attrs={
            'class': 'form-control appearance-none w-60 py-2.5 px-4 text-coolGray-900 text-base font-normal bg-white border outline-none border-coolGray-200 focus:border-green-500 rounded-lg shadow-input'})
    )
    is_perishable = forms.BooleanField(
        label="Is Perishable",
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input border outline-none border-coolGray-200 focus:border-green-500 rounded-sm'})
    )

    class Meta:
        model = Donation
        fields = ['RestaurantID', 'is_perishable']


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
        fields = ['MealType', 'MealQuantityPlates', 'pickup_location']


from django import forms
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


class NonPerishableDonationForm(forms.ModelForm):
    MealTitle = forms.CharField(
        label="Meal Title",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control mb-5'}),
        validators=[MinLengthValidator(1), validate_text_with_spaces_and_punctuation, validate_letters_only],
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
        fields = ['MealTitle', 'MealDescription', 'MealQuantityKgs', 'pickup_location']


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
