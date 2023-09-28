import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import validate_email


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-60 px-4 py-2.5 text-base text-coolGray-900 font-normal outline-none focus:border-green-500 border border-coolGray-200 rounded-lg shadow-input',
            'required': 'required',
        }),
    )
    new_password1 = forms.CharField(
        label="New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-60 px-4 py-2.5 text-base text-coolGray-900 font-normal outline-none focus:border-green-500 border border-coolGray-200 rounded-lg shadow-input',
            'required': 'required',
        }),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-60 px-4 py-2.5 text-base text-coolGray-900 font-normal outline-none focus:border-green-500 border border-coolGray-200 rounded-lg shadow-input',
            'required': 'required',
        }),
    )


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

        # Add additional validation for the profile photo if needed

        return photo