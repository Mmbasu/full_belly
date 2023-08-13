import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm


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