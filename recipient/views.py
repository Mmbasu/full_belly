from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt

from users.models import CustomUser
from .forms import DriverCreationForm
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse

from .models import Organization, Driver


# Create your views here.

def dashboard(request):
    return render(request, 'recipient/dashboard.html')


def restaurants(request):
    return render(request, 'recipient/restaurants.html')


def add_restaurant(request):
    return render(request, 'recipient/add_restaurant.html')


def edit_restaurant(request):
    return render(request, 'recipient/edit_restaurant.html')


def donate(request):
    return render(request, 'recipient/donate_0.html')


def ngo_details(request):
    return render(request, 'recipient/ngo_details.html')


def history(request):
    return render(request, 'recipient/history.html')


def history_details(request):
    return render(request, 'recipient/history_details.html')


def make_donation(request):
    return render(request, 'recipient/donate_1.html')


def profile(request):
    return render(request, 'recipient/profile.html')


def support(request):
    return render(request, 'recipient/support.html')


def raise_issue(request):
    return render(request, 'recipient/raise_issue.html')


def edit_profile(request):
    return render(request, 'recipient/edit_profile.html')


def change_password(request):
    return render(request, 'recipient/change_password.html')


def about(request):
    return render(request, 'recipient/about.html')


def messaging(request):
    return render(request, 'recipient/messaging.html')


def send_message(request):
    return render(request, 'recipient/send_message.html')


def reply(request):
    return render(request, 'recipient/reply.html')


def notification(request):
    return render(request, 'recipient/notification.html')


def help_documentation(request):
    return render(request, 'recipient/help_documentation.html')


def settings(request):
    return render(request, 'recipient/settings.html')


def donation(request):
    return render(request, 'recipient/donation.html')


def request_donation(request):
    return render(request, 'recipient/request_donation.html')


def request_donation_1(request):
    return render(request, 'recipient/request_donation_1.html')


def donation_details(request):
    return render(request, 'recipient/donation_details.html')


def edit_donation_request(request):
    return render(request, 'recipient/edit_donation_request.html')


def accepted_donation_details(request):
    return render(request, 'recipient/accepted_donation_details.html')


def restaurant_details(request):
    return render(request, 'recipient/restaurant_details.html')


def edit_ngo_details(request):
    return render(request, 'recipient/edit_ngo_details.html')


def driver_list(request):
    drivers = Driver.objects.all()  # Retrieve all drivers from the database
    return render(request, 'recipient/driver.html', {'drivers': drivers})


from django.shortcuts import render, get_object_or_404
from .models import Driver
from .forms import DriverCreationForm


def edit_driver(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)

    if request.method == 'POST':
        form = DriverCreationForm(request.POST, request.FILES,
                                  instance=driver)  # Include request.FILES to handle the image file
        if form.is_valid():
            form.save()
            return redirect('recipient:driver_details', driver_id=driver_id)
    else:
        form = DriverCreationForm(instance=driver)

    # Exclude 'password' and 'Photo' fields from the form
    form.fields.pop('password1')
    form.fields.pop('password2')
    form.fields.pop('Photo')

    context = {
        'driver': driver,
        'form': form,
        'driver_id': driver_id,
    }

    return render(request, 'recipient/edit_driver.html', context)


def driver_details(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    context = {'driver': driver}
    return render(request, 'recipient/driver_details.html', context)


# def add_driver(request):
#     if request.method == 'POST':
#         form = DriverCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             driver = form.save(commit=False)
#             driver.save()
#
#             # # Send the activation email
#             # subject = 'Activate your Account'
#             # activate_url = request.build_absolute_uri(reverse('users:activate_account',
#             #                                                   args=[urlsafe_base64_encode(force_bytes(driver.pk)),
#             #                                                         driver.activation_token]))
#             # context = {'token': driver.activation_token, 'activate_url': activate_url, 'user': driver}
#             # html_content = render_to_string('users/activation.html', context)
#             # msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [driver.email])
#             # msg.content_subtype = 'html'
#             # msg.send(fail_silently=True)
#
#             return JsonResponse({'success': True})
#         else:
#             errors = form.errors
#             return JsonResponse({'success': False, 'errors': errors})
#     else:
#         form = DriverCreationForm()
#     return render(request, 'recipient/add_driver.html', {'form': form})


def add_driver(request):
    if request.method == 'POST':
        form = DriverCreationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a corresponding CustomUser instance
            user = CustomUser.objects.create_user(
                email=form.cleaned_data['Email'],
                username=form.cleaned_data['Username'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                role='driver',
                is_active=True
            )

            # Create a Driver instance and associate it with the CustomUser
            driver = Driver.objects.create(
                DriverID=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                Username=form.cleaned_data['Username'],
                Email=form.cleaned_data['Email'],
                Phone=form.cleaned_data['Phone'],
                Photo=form.cleaned_data['Photo'],
                DriverIDNumber=form.cleaned_data['DriverIDNumber'],
                DrivingLicenseNumber=form.cleaned_data['DrivingLicenseNumber'],
                CarNumberPlate=form.cleaned_data['CarNumberPlate'],
                OrganizationID=form.cleaned_data['OrganizationID'],
            )

            return JsonResponse({'success': True})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = DriverCreationForm()
    return render(request, 'recipient/add_driver.html', {'form': form})


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Driver


@require_POST
def delete_driver(request, driver_id):
    try:
        driver = get_object_or_404(Driver, DriverID=driver_id)
        driver.delete()
        return JsonResponse({'success': True})
    except Driver.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Driver not found'})



def logout_view(request):
    logout(request)
    return redirect('users:login')
