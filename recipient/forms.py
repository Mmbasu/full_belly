from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from .models import Driver, Organization



class DriverCreationForm(UserCreationForm):
    Email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),
    Username = forms.CharField(label="Username", required=True, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),
    first_name = forms.CharField(label="First Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),
    last_name = forms.CharField(label="Last Name", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),
    Phone = forms.CharField(label="Phone", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),

    Photo = forms.ImageField(label=" Driver Photo", widget=forms.ClearableFileInput(
        attrs={'class': 'form-control mb-5'}
    )),

    DriverIDNumber = forms.CharField(label="Driver ID Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),
    DrivingLicenseNumber = forms.CharField(label="Driving License Number", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5', }
    )),
    CarNumberPlate = forms.CharField(label="Car Number Plate", widget=forms.TextInput(
        attrs={'class': 'form-control mb-5'}
    )),

    # organization_choices = [(org.OrganizationID, org.Name) for org in Organization.objects.all()]

    OrganizationID = forms.ModelChoiceField(
        label="Organization ID",
        queryset=Organization.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control mb-5'})
    ),

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5'}
    )),
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control mb-5'}
    )),

    # Status = forms.ChoiceField(
    #     label="Status",
    #     choices=Driver.STATUS_CHOICES,
    #     initial='idle',
    #     widget=forms.Select(attrs={'class': 'form-control mb-5'}),
    # )

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    class Meta:
        model = Driver
        fields = (
            'first_name', 'last_name', 'Email', 'Username', 'Phone', 'Photo', 'DriverIDNumber', 'DrivingLicenseNumber', 'CarNumberPlate',
            'OrganizationID', 'password1', 'password2')
