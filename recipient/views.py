from django.contrib.auth import logout, update_session_auth_hash
from django.views import View
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle
from driver.models import Delivery
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from donor.models import Donation, PerishableDonation, NonPerishableDonation
from recipient.models import RecipientDelivery, Driver
from .decorators import requires_password_change


@login_required
@requires_password_change
def dashboard(request):
    recipient = request.user

    delivered_deliveries = RecipientDelivery.objects.filter(ManagerID=recipient, Status='delivered')

    try:
        # Get the organization managed by the logged-in user
        organization = Organization.objects.get(ManagerID=recipient)

        # Calculate Food Received for the specific organization (sum of MealQuantityKgs from PerishableDonation and NonPerishableDonation)
        perishable_food_received = PerishableDonation.objects.filter(
            Donation__Status='delivered', Donation__Organization=organization).aggregate(
            total_plates=Sum('MealQuantityPlates'))['total_plates'] or 0

        non_perishable_food_received = NonPerishableDonation.objects.filter(
            Donation__Status='delivered', Donation__Organization=organization).aggregate(
            total_kgs=Sum('MealQuantityKgs'))['total_kgs'] or 0

    except Organization.DoesNotExist:
        perishable_food_received = 0
        non_perishable_food_received = 0

    # Limiting donations to 3 and ordering by date_delivered in descending order
    perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=True).order_by(
        '-DonationID__date_delivered')[:3]
    non_perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=False).order_by(
        '-DonationID__date_delivered')[:3]

    # Calculate Food Pickups (count of delivered deliveries)
    food_pickups = RecipientDelivery.objects.filter(ManagerID=recipient, Status='delivered').count()

    # Calculate Restaurants Served (count of distinct RestaurantIDs in delivered donations)
    restaurants_served = Donation.objects.filter(Organization__ManagerID=recipient, Status='delivered').values(
        'RestaurantID').distinct().count()

    # Calculate NGO Drivers (count of drivers associated with the recipient)
    ngo_drivers = Driver.objects.filter(OrganizationID__ManagerID=recipient).count()

    context = {
        'perishable_deliveries': perishable_deliveries,
        'non_perishable_deliveries': non_perishable_deliveries,
        'perishable_food_received': perishable_food_received,
        'non_perishable_food_received': non_perishable_food_received,
        'food_pickups': food_pickups,
        'restaurants_served': restaurants_served,
        'ngo_drivers': ngo_drivers,
    }

    return render(request, 'recipient/dashboard.html', context)


@login_required
@requires_password_change
def restaurants(request):
    return render(request, 'recipient/restaurants.html')


@login_required
@requires_password_change
def add_restaurant(request):
    return render(request, 'recipient/add_restaurant.html')


@login_required
@requires_password_change
def edit_restaurant(request):
    return render(request, 'recipient/edit_restaurant.html')


@login_required
@requires_password_change
def donate(request):
    return render(request, 'recipient/donate_0.html')



from django.http import JsonResponse

@login_required
@requires_password_change
def ngo_details(request):
    try:
        organization = Organization.objects.annotate(avg_rating=Avg('organizationrating__rating'),
                                                     num_ratings=Count('organizationrating__rating')).get(
            ManagerID=request.user)
        form = OrganizationForm(instance=organization)
        template = 'recipient/ngo_details.html'
    except Organization.DoesNotExist:
        organization = None
        form = OrganizationForm()
        template = 'recipient/add_organization.html'

    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.ManagerID = request.user
            organization.save()
            return JsonResponse({'success': True})  # Return success: True
        else:
            # Form validation failed, return errors in JSON response
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = [error for error in error_list]
            return JsonResponse({'success': False, 'errors': errors})

    context = {
        'organization': organization,
        'form': form,
    }
    return render(request, template, context)



@login_required
@requires_password_change
def history(request):
    recipient = request.user

    delivered_deliveries = RecipientDelivery.objects.filter(ManagerID=recipient, Status='delivered')
    perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=True, Status='delivered')
    non_perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=False, Status='delivered')

    context = {
        'delivered_deliveries': delivered_deliveries,
        'perishable_deliveries': perishable_deliveries,
        'non_perishable_deliveries': non_perishable_deliveries,
    }

    return render(request, 'recipient/history.html', context)



class MarkAsDeliveredView(View):
    def post(self, request, donation_id):
        donation = get_object_or_404(Donation, pk=donation_id)
        if donation.Status != 'delivered':
            # Update related models
            with transaction.atomic():
                # Mark the donation as delivered
                donation.Status = 'delivered'

                # Record the current date and time as the date_delivered
                donation.date_delivered = timezone.now()

                donation.save()

                donation.delivery_set.update(Status='delivered')
                donation.recipientdelivery_set.update(Status='delivered')

                # Update driver status to "idle"
                if donation.driver:
                    driver = donation.driver
                    driver.Status = 'idle'
                    driver.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'The donation is already marked as delivered.'})



@login_required
@requires_password_change
def history_details(request, donation_id):
    recipient_deliveries = RecipientDelivery.objects.filter(DonationID=donation_id)
    donation = get_object_or_404(Donation, DonationID=donation_id)

    context = {
        'donation': donation,
        'recipient_deliveries': recipient_deliveries,
    }

    return render(request, 'recipient/history_details.html', context)


@login_required
@requires_password_change
def make_donation(request):
    return render(request, 'recipient/donate_1.html')


@login_required
@requires_password_change
def profile(request):
    user = request.user
    recipient = user.recipient.first()

    context = {
        'user': user,
        'recipient': recipient,
    }
    return render(request, 'recipient/profile.html', context)


@login_required
@requires_password_change
def support(request):
    return render(request, 'recipient/support.html')


@login_required
@requires_password_change
def raise_issue(request):
    return render(request, 'recipient/raise_issue.html')


from .forms import ProfileForm, DriverUpdateForm, DriverCreationForm, PerishableDonationForm, NonPerishableDonationForm, \
    ChangePasswordForm

from django.http import JsonResponse


@requires_password_change
@login_required
def edit_profile(request):
    user = request.user
    data = {}

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.twitter_link = form.cleaned_data.get("twitter_link")
            user.instagram_link = form.cleaned_data.get("instagram_link")
            user.facebook_link = form.cleaned_data.get("facebook_link")
            user.save()
            data['message'] = "Profile updated successfully"
        else:
            data['errors'] = form.errors
    else:
        form = ProfileForm(instance=user)

    if request.method == 'POST':
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    else:
        context = {"form": form}
        return render(request, "recipient/edit_profile.html", context)


@login_required
@requires_password_change
def accept_donation(request, donation_id):
    try:
        with transaction.atomic():
            donation = get_object_or_404(Donation, pk=donation_id)
            donation.accept_donation()  # Utilize the accept_donation method in the model
            donation.save()

            return JsonResponse({'success': True})
    except Donation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Donation not found'})



@login_required
@requires_password_change
def change_password(request):
    return render(request, 'recipient/change_password.html')


@login_required
@requires_password_change
def about(request):
    return render(request, 'recipient/about.html')


@login_required
@requires_password_change
def messaging(request):
    return render(request, 'recipient/messaging.html')


@login_required
@requires_password_change
def send_message(request):
    return render(request, 'recipient/send_message.html')


@login_required
@requires_password_change
def reply(request):
    return render(request, 'recipient/reply.html')


@login_required
@requires_password_change
def notification(request):
    return render(request, 'recipient/notification.html')


@login_required
@requires_password_change
def help_documentation(request):
    return render(request, 'recipient/help_documentation.html')


@login_required
def settings_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            return JsonResponse({'success': True})
        else:
            errors = form.errors
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = ChangePasswordForm(request.user)

    # Determine whether to show the delete section
    show_delete_section = not request.user.check_password(request.user.temporary_password)

    # Include show_delete_section in the context dictionary
    context = {'form': form, 'show_delete_section': show_delete_section}

    return render(request, 'recipient/settings.html', context)




from django.utils import timezone
from django.core.management import call_command
from django.db import transaction


@login_required
@requires_password_change
def donation(request):

    call_command('cleardonations')

    user = request.user
    accepted_donations = Donation.objects.filter(
        Q(is_accepted=True, Organization__ManagerID=user, Status='pending') |
        Q(is_accepted=True, Organization__ManagerID=user, Status='Intransit')
    )

    # Update the accepted donations if not scheduled within 10 minutes
    for donation in accepted_donations:
        if donation.is_accepted and not donation.is_scheduled:
            if donation.accepted_timestamp:
                elapsed_time = timezone.now() - donation.accepted_timestamp
                if elapsed_time.total_seconds() > 600:  # 10 minutes in seconds
                    donation.is_accepted = False
                    donation.accepted_timestamp = None  # Reset the accepted timestamp
                    donation.save()

                    donation.remaining_time = 0  # Set remaining time to 0 if expired
                else:
                    donation.remaining_time = 600 - elapsed_time.total_seconds()  # Store remaining time in seconds
            else:
                donation.remaining_time = 600  # Set full remaining time if accepted_timestamp is None

    ngo_requested_donations = Donation.objects.filter(ngo_requested=True, Organization__ManagerID=user,
                                                      is_accepted=False)
    pending_donations = Donation.objects.filter(
        Q(is_accepted=False, Organization__ManagerID=user, ngo_requested=False) | Q(Organization__Name='all'))

    return render(request, 'recipient/donation.html',
                  {'accepted_donations': accepted_donations, 'pending_donations': pending_donations,
                   'ngo_requested_donations': ngo_requested_donations})




@login_required
@requires_password_change
def get_ngos_drivers(request):
    if request.user.is_authenticated and request.user.role == 'recipient':
        # Get the organization of the logged-in user (assuming the manager is always a recipient)
        organization = Organization.objects.get(ManagerID=request.user)

        # Get the drivers associated with the organization
        drivers = Driver.objects.filter(OrganizationID=organization)

        # Prepare the data to be sent as JSON
        data = [{'id': driver.DriverID.id, 'name': f"{driver.first_name} {driver.last_name}"} for driver in drivers]

        return JsonResponse(data, safe=False)

    return JsonResponse([], safe=False)


@login_required
@requires_password_change
def save_schedule_pickup(request):
    if request.method == 'POST':
        donation_id = request.POST.get('donation_id')
        pickup_time = request.POST.get('pickup_time')
        driver_id = request.POST.get('driver_id')

        try:
            donation = get_object_or_404(Donation, pk=donation_id)
            driver = get_object_or_404(Driver, pk=driver_id)

            # Use a transaction to ensure that both objects are saved or none at all
            with transaction.atomic():
                # Create a new RecipientDelivery object
                delivery = RecipientDelivery.objects.create(
                    ManagerID=request.user,
                    DonationID=donation,
                    DriverID=driver,
                    PickupDateTime=pickup_time,
                    Status='pending'
                )

                # Update the Donation object with the pickup time, driver, and scheduled status
                donation.pickup_time = pickup_time
                donation.driver = driver
                donation.is_scheduled = True
                donation.save()

                # Access the correct pickup_location based on is_perishable
                pickup_location = donation.RestaurantID.Location
                if donation.is_perishable:
                    pickup_location = delivery.DonationID.perishabledonation.pickup_location
                else:
                    pickup_location = delivery.DonationID.nonperishabledonation.pickup_location

                # Create a new Delivery object using the RecipientDelivery object's data
                new_delivery = Delivery.objects.create(
                    DonationID=donation,
                    DeliveryID=delivery,  # Set DeliveryID to the RecipientDelivery object's ID
                    PickupDateTime=pickup_time,
                    PickupPoint=pickup_location,
                    DriverID=driver,
                    Status='pending',  # Set the initial status for the new Delivery object
                )

            return JsonResponse({'message': 'Pickup scheduled successfully.'}, status=200)
        except Donation.DoesNotExist:
            return JsonResponse({'error': 'Donation not found.'}, status=404)
        except Driver.DoesNotExist:
            return JsonResponse({'error': 'Driver not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



from django.db.models import Avg, Count, Q, Sum

from django.db.models import F


@login_required
@requires_password_change
def request_donation(request):
    top_restaurants = Restaurant.objects.annotate(avg_rating=Avg('restaurantrating__rating'),
                                                  num_ratings=Count('restaurantrating__rating')).order_by(
        '-avg_rating')[:5]

    top_restaurant_pks = [restaurant.pk for restaurant in top_restaurants]

    other_restaurants = Restaurant.objects.annotate(avg_rating=Avg('restaurantrating__rating'),
                                                    num_ratings=Count('restaurantrating__rating')).filter(
        ~Q(pk__in=top_restaurant_pks))

    context = {
        'top_restaurants': top_restaurants,
        'other_restaurants': other_restaurants,
    }

    return render(request, 'recipient/request_donation.html', context)


from django.shortcuts import render, redirect
from .forms import DonationForm
from donor.models import Donation
from recipient.models import Organization


@login_required
@requires_password_change
def request_donation_1(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)

            # Find the organization whose ManagerID is the logged-in user
            organization = Organization.objects.get(ManagerID=request.user)

            # Associate the organization with the donation
            donation.Organization = organization

            donation.save()  # Save the donation record to the database

            # Set ngo_requested field to True after saving the donation record
            donation.ngo_requested = True
            donation.save()

            if donation.is_perishable:
                return redirect('recipient:perishable_donation_create', donation_id=donation.pk)
            else:
                return redirect('recipient:non_perishable_donation_create', donation_id=donation.pk)
    else:
        form = DonationForm()

    return render(request, 'recipient/request_donation_1.html', {'form': form})


@requires_password_change
@login_required
def perishable_donation_create(request, donation_id):
    donation = Donation.objects.get(pk=donation_id)
    perishable_donation_form = PerishableDonationForm()

    if request.method == 'POST':
        perishable_donation_form = PerishableDonationForm(request.POST, request.FILES)
        if perishable_donation_form.is_valid():
            perishable_donation = perishable_donation_form.save(commit=False)
            perishable_donation.Donation = donation
            perishable_donation.save()
            return JsonResponse({'success': True})
        else:
            errors = {}
            for field, error_list in perishable_donation_form.errors.items():
                errors[field] = [error for error in error_list]
            return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'recipient/perishable_donation_create.html',
                  {'donation': donation, 'perishable_donation_form': perishable_donation_form})


@requires_password_change
@login_required
def non_perishable_donation_create(request, donation_id):
    donation = Donation.objects.get(pk=donation_id)
    non_perishable_donation_form = NonPerishableDonationForm()

    if request.method == 'POST':
        non_perishable_donation_form = NonPerishableDonationForm(request.POST, request.FILES)
        if non_perishable_donation_form.is_valid():
            non_perishable_donation = non_perishable_donation_form.save(commit=False)
            non_perishable_donation.Donation = donation
            non_perishable_donation.save()
            return JsonResponse({'success': True})

        # Form is not valid, prepare errors in JSON format
        errors = {}
        for field, error_list in non_perishable_donation_form.errors.items():
            errors[field] = [error for error in error_list]
        return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'recipient/non_perishable_donation_create.html',
                  {'donation': donation, 'non_perishable_donation_form': non_perishable_donation_form})


@login_required
@requires_password_change
def donation_details(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)

    return render(request, 'recipient/donation_details.html', {'donation': donation})


from django.http import JsonResponse

@login_required
@requires_password_change
def edit_donation_request(request, donation_id):
    perishable_donation = None
    non_perishable_donation = None
    donation_form = None

    try:
        perishable_donation = PerishableDonation.objects.get(Donation_id=donation_id)
        donation_form = PerishableDonationForm(request.POST or None, request.FILES or None,
                                               instance=perishable_donation)
    except PerishableDonation.DoesNotExist:
        try:
            non_perishable_donation = NonPerishableDonation.objects.get(Donation_id=donation_id)
            donation_form = NonPerishableDonationForm(request.POST or None, request.FILES or None,
                                                      instance=non_perishable_donation)
        except NonPerishableDonation.DoesNotExist:
            pass

    if request.method == 'POST':
        if donation_form and donation_form.is_valid():
            donation_form.save()
            return JsonResponse({'success': True})
        else:
            # Form validation failed, return errors in JSON response
            errors = {field: error[0] for field, error in donation_form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})

    return render(request, 'recipient/edit_donation_request.html', {
        'donation_form': donation_form,
        'perishable_donation': perishable_donation,
        'non_perishable_donation': non_perishable_donation,
    })




@login_required
@requires_password_change
def accepted_donation_details(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id, is_accepted=True)
    return render(request, 'recipient/accepted_donation_details.html', {'donation': donation})


from django.db.models import Avg
from donor.models import Restaurant


@login_required
@requires_password_change
def restaurant_details(request, restaurant_id):
    restaurant = Restaurant.objects.annotate(avg_rating=Avg('restaurantrating__rating'),
                                             num_ratings=Count('restaurantrating__rating')).get(
        RestaurantID=restaurant_id)
    return render(request, 'recipient/restaurant_details.html', {'restaurant': restaurant})


from .forms import OrganizationForm

@login_required
@requires_password_change
def edit_ngo_details(request):
    organization = Organization.objects.get(ManagerID=request.user)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "NGO edited successfully"})
        else:
            # Form validation failed, return errors in JSON response
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
            return JsonResponse({"errors": errors}, status=400)
    else:
        form = OrganizationForm(instance=organization)

    context = {'form': form}
    return render(request, 'recipient/edit_ngo_details.html', context)



@login_required
@requires_password_change
def driver_list(request):
    try:
        organization = Organization.objects.get(ManagerID=request.user)
        drivers = Driver.objects.filter(OrganizationID=organization)
    except Organization.DoesNotExist:
        organization = None
        drivers = []

    context = {'organization': organization, 'drivers': drivers}
    return render(request, 'recipient/driver.html', context)


from django.http import JsonResponse

from django.http import JsonResponse
from .forms import DriverUpdateForm
from .models import Driver
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
@requires_password_change
def edit_driver(request, driver_id):
    driver = Driver.objects.get(pk=driver_id)
    user = driver.DriverID

    if request.method == 'POST':
        form = DriverUpdateForm(request.POST, request.FILES, instance=driver)
        if form.is_valid():
            form.save()

            # Update the corresponding User instance
            user.email = form.cleaned_data['Email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone = form.cleaned_data['phone']
            user.photo = form.cleaned_data['photo']
            user.save()

            return JsonResponse({'success': True})
        else:
            # Form is not valid, collect error messages
            form_errors = form.errors
            errors = {field: [error for error in field_errors] for field, field_errors in form_errors.items()}

            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = DriverUpdateForm(instance=driver)

    context = {'form': form, 'driver_id': driver_id}
    return render(request, 'recipient/edit_driver.html', context)




@login_required
@requires_password_change
def driver_details(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    context = {'driver': driver}
    return render(request, 'recipient/driver_details.html', context)


@login_required
@requires_password_change
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
                phone=form.cleaned_data['phone'],
                role='driver',
                is_active=True
            )
            # Get the organization managed by the currently logged in user
            organization = Organization.objects.get(ManagerID=request.user)

            # Create a Driver instance and associate it with the CustomUser and the organization
            driver = Driver.objects.create(
                DriverID=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                Username=form.cleaned_data['Username'],
                Email=form.cleaned_data['Email'],
                phone=form.cleaned_data['phone'],
                photo=form.cleaned_data['photo'],
                DriverIDNumber=form.cleaned_data['DriverIDNumber'],
                DrivingLicenseNumber=form.cleaned_data['DrivingLicenseNumber'],
                CarNumberPlate=form.cleaned_data['CarNumberPlate'],
                OrganizationID=organization,
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
@login_required
@requires_password_change
def delete_driver(request, driver_id):
    try:
        driver = get_object_or_404(Driver, DriverID=driver_id)

        # Retrieve the associated user instance
        user = driver.DriverID

        # Delete the user account
        user.delete()

        # Delete the driver
        driver.delete()

        return JsonResponse({'success': True})
    except Driver.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Driver not found'})
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'User not found'})


from django.db import transaction

@requires_password_change
@login_required
def delete_donation(request, donation_id):
    try:
        with transaction.atomic():
            donation = get_object_or_404(Donation, pk=donation_id)

            if donation.ngo_requested:
                if donation.is_perishable:
                    perishable_donation = donation.perishabledonation
                    perishable_donation.delete()
                else:
                    non_perishable_donation = donation.nonperishabledonation
                    non_perishable_donation.delete()

            donation.delete()

            return JsonResponse({'success': True})
    except Donation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Donation not found'})

@requires_password_change
def logout_view(request):
    logout(request)
    return redirect('users:login')


from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class DonationReportView(View):

    def get(self, request, donation_id):
        donation = Donation.objects.get(DonationID=donation_id)

        # Create a response object with PDF content type
        response = HttpResponse(content_type='application/pdf')

        # Set the filename for the downloaded PDF file
        response['Content-Disposition'] = 'attachment; filename="donation_received_report.pdf"'

        # Create the PDF document
        p = canvas.Canvas(response, pagesize=letter)

        # Set the font styles
        p.setFont("Helvetica-Bold", 16)  # Use a bold font and increase the font size

        # Define the y-coordinate for the first line of text
        y = 750  # Adjust the y-coordinate to match the template's layout

        # Add the company logo
        logo_path = 'https://i.ibb.co/wKwTF3T/Screenshot-from-2023-03-18-08-54-04.png'
        image_width = 150
        image_height = 150
        image_x = (p._pagesize[0] - image_width) / 2  # Center the image horizontally
        image_y = p._pagesize[
                      1] - image_height - inch - 20  # Place the image at the top, leaving some space before the text

        p.drawImage(logo_path, image_x, image_y, width=image_width, height=image_height, preserveAspectRatio=True)

        # Add the "Delivery Report" text in bold
        p.setFont("Helvetica-Bold", 14)
        p.drawString(250, image_y - 40, "Donation Report")  # Adjust the y-coordinate for the text

        # Generate the PDF content with delivery details
        data = [
            ["ID", donation.DonationID],
            ["Restaurant", donation.RestaurantID.Name],
            ["NGO", donation.Organization],
            ["Meal",
             donation.perishabledonation.MealType if donation.is_perishable else donation.nonperishabledonation.MealTitle],
            ["Quantity",
             f"{donation.perishabledonation.MealQuantityPlates} Plates" if donation.is_perishable else f"{donation.nonperishabledonation.MealQuantityKgs} Kgs"],
            ["Food Type", "Perishable Food" if donation.is_perishable else "Non-Perishable Food"],
            ["Assigned Driver", donation.driver],
            ["Pickup Location",
             donation.perishabledonation.pickup_location if donation.is_perishable else donation.nonperishabledonation.MealTitle],
        ]

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#EEEEEE")),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor("#000000")),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, -1), 12),
            ('BOTTOMPADDING', (0, 0), (0, -1), 12),
            ('BACKGROUND', (1, 0), (-1, -1), colors.HexColor("#FFFFFF")),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#AAAAAA")),
        ])

        table = Table(data)
        table.setStyle(table_style)
        table.wrapOn(p, 450, 200)  # Adjust the table width
        table.drawOn(p, 75, image_y - 300)  # Adjust the y-coordinate for the table

        # Set the font styles for the additional text
        p.setFont("Helvetica", 12)  # Use a smaller font size

        additional_text = [
            "Thank you for receiving the donation!",
            HexColor("#000000"),  # Hex code for black color
            "Terms and Conditions:",
            "- The received goods should meet the required standards.",
            "- Any discrepancies or issues should be reported within 24 hours.",
            "- The donation is subject to acceptance by the receiving party.",
            "- Any unauthorized use or distribution is prohibited.",
        ]

        # Define the y-coordinate for the additional text
        y_additional_text = image_y - 400  # Adjust the y-coordinate

        for text in additional_text:
            if isinstance(text, str):
                p.setFont("Helvetica-Bold", 12)
                if text == "Thank you for receiving the donation!":
                    p.setFillColor(HexColor("#2BA19A"))  # Hex code for the desired color
                else:
                    p.setFillColor(HexColor("#000000"))  # Hex code for black color
                p.drawString(50, y_additional_text, text)
            else:
                p.setFillColor(text)
            y_additional_text -= 15

        # Save the PDF document
        p.showPage()
        p.save()

        return response


import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from donor.models import RestaurantRating, Donation


@csrf_exempt
@require_POST
@requires_password_change
def rate_restaurant(request, donation_id):
    user = request.user
    try:
        donation = Donation.objects.get(pk=donation_id)
        restaurant = donation.RestaurantID
        organization = donation.Organization

    except Donation.DoesNotExist:
        return JsonResponse({'message': 'Invalid donation or restaurant not found for the current user.'})

    if restaurant and organization:
        # Parse the JSON data from the request body
        data = json.loads(request.body)
        rating_value = data.get('rating')

        print('Rating Value:', rating_value)

        if rating_value is not None:
            # Save the rating in the database
            rating = RestaurantRating.objects.create(user=user, restaurant=restaurant, organization=organization,
                                                     donation_id=donation_id,
                                                     rated_entity_type='RESTAURANT', rating=rating_value)
            rating.save()

            return JsonResponse({'message': 'Rating saved successfully.'})
        else:
            return JsonResponse({'message': 'Rating value is missing or invalid.'})
    else:
        return JsonResponse({'message': 'Restaurant or organization not found for the current user.'})


from django.http import JsonResponse
from donor.models import RestaurantRating, Donation

@requires_password_change
def check_rating_exists(request, donation_id):
    user = request.user
    try:
        donation = Donation.objects.get(pk=donation_id)

    except Donation.DoesNotExist:
        return JsonResponse({'exists': False})

    # Check if the rating exists for the current user and donation
    rating_exists = RestaurantRating.objects.filter(user=user, donation=donation).exists()
    return JsonResponse({'exists': rating_exists})




import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.conf import settings


@csrf_exempt
@login_required
@requires_password_change
def send_deletion_code(request):
    if request.method == 'POST':
        # Generate a random 5-digit deletion code
        deletion_code = ''.join([str(random.randint(0, 9)) for _ in range(5)])

        # Update the user's profile with the deletion code
        user = request.user
        user.delete_account_code = deletion_code
        user.save()

        # Send the deletion code via email
        subject = 'Account Deletion Code'
        html_content = render_to_string('recipient/deletion_code_email.html', {'deletion_code': deletion_code})

        msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)  # Set fail_silently to False for debugging purposes
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@csrf_exempt
@login_required
@requires_password_change
def delete_account(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            deletion_code = data.get('deletionCode')
            user = request.user

            if user.delete_account_code == deletion_code:
                user.delete()  # Delete the user account
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST  # Require POST requests only for this view
def check_password_view(request):
    current_password = request.POST.get('password', '')  # Get the password from the POST data

    # Check if the provided password matches the user's current password
    if request.user.check_password(current_password):
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})




