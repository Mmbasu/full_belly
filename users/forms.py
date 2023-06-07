from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.db.models import Q
from users.models import CustomUser
from django import forms
from django.contrib.auth.forms import SetPasswordForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'E-mail address'}
    ))
    username = forms.CharField(required=True, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Username'}
    ))
    first_name = forms.CharField(label="First Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'First Name'}
    ))
    last_name = forms.CharField(label="Last Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Last Name'}
    ))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Password'}
    ))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Confirm password'}
    ))

    role = forms.ChoiceField(
        label="Role",
        choices=CustomUser.ROLE_CHOICES,
        initial='donor',
        widget=forms.Select(attrs={'class': 'form-control mb-5'}),
        required=True  # Add this line to make the field required
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('donor', 'Donor'), ('recipient', 'Recipient')]

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control mb-5', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control mb-5', 'placeholder': 'Password'})
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct username and password. Note that both fields may be case-sensitive. goodluck"
        ),
        'inactive': _("Please activate your account."),
    }


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,
        help_text=_("Enter your new password."),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=_("Enter the same password as before, for verification."),
    )
