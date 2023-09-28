from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.db.models import Q

from donor.validators import validate_text_with_spaces_and_punctuation
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
    username = forms.CharField(required=True, validators=[validate_text_with_spaces_and_punctuation], max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Username'},
    ))

    phone = forms.CharField(required=True, max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Phone Number'}
    ))

    first_name = forms.CharField(label="First Name", validators=[validate_text_with_spaces_and_punctuation], max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'First Name'}
    ))
    last_name = forms.CharField(label="Last Name", validators=[validate_text_with_spaces_and_punctuation], max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Last Name'}
    ))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Password', 'required': 'required'}
    ))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5', 'placeholder': 'Confirm password','required': 'required'}
    ))

    role = forms.ChoiceField(
        label="Role",
        choices=CustomUser.ROLE_CHOICES,
        initial='donor',
        widget=forms.Select(attrs={'class': 'form-control mb-5'}),
        required=True  # Add this line to make the field required
    )

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
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("This email address is already in use.")
        except forms.ValidationError:
            raise forms.ValidationError("Invalid email address.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Phone number should be numerical and contain 10 digits")
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('donor', 'Donor'), ('recipient', 'Recipient')]

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'phone', 'password2')


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
            "Please enter a correct username and password. Note that both fields may be case-sensitive."
        ),
        'inactive': _("Please activate your account."),
        'invalid_login_attempts': _(
            "You have exceeded the maximum login attempts at this time. Try again after 1 minute"
        ),
    }


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),

    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Invalid email address.")

        return email


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



from django.core.validators import validate_email

class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
        error_messages={'invalid': 'Invalid email address.'},
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Invalid email address.")

        return email
