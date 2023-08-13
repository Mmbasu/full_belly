from django.contrib.auth import update_session_auth_hash, logout
from django.db import transaction
from django.db.models import Q, Avg, Count, Sum
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.core.management import call_command
from django.db import transaction

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from reportlab.lib.colors import HexColor
from reportlab.platypus import Table, TableStyle

from recipient.models import Organization, OrganizationRating
from .forms import ChangePasswordForm, ProfileForm, NonPerishableDonationForm, PerishableDonationForm
from .models import Donation, Restaurant, NonPerishableDonation, PerishableDonation
from donor.decorators import requires_password_change



@requires_password_change
@login_required
def dashboard(request):
    donor = request.user

    # Retrieve all restaurants owned by the donor
    restaurants_owned_by_donor = Restaurant.objects.filter(ManagerID=donor)

    # Retrieve donations for all restaurants owned by the donor
    donations = Donation.objects.filter(RestaurantID__in=restaurants_owned_by_donor, Status='delivered')

    # Calculate Food Donated (sum of MealQuantityKgs from PerishableDonation and NonPerishableDonation)
    perishable_food_donated = PerishableDonation.objects.filter(Donation__in=donations).aggregate(
        total_plates=Sum('MealQuantityPlates'))['total_plates'] or 0

    non_perishable_food_donated = NonPerishableDonation.objects.filter(Donation__in=donations).aggregate(
        total_kgs=Sum('MealQuantityKgs'))['total_kgs'] or 0

    # Calculate Food Pickups (count of delivered deliveries)
    food_pickups = Donation.objects.filter(DonationID__in=donations, Status='delivered').count()

    # Calculate NGO's Served (count of distinct OrganizationIDs in delivered donations)
    ngos_served = Donation.objects.filter(RestaurantID__in=restaurants_owned_by_donor, Status='delivered').values(
        'Organization').distinct().count()

    # Count the number of restaurants managed by the logged-in user
    num_restaurants_managed = restaurants_owned_by_donor.count()

    if num_restaurants_managed == 0:
        num_restaurants_managed = 0  # Set the number to zero if there are no restaurants

    # Separate perishable and non-perishable donations
    perishable_donations = donations.filter(is_perishable=True).order_by('-date_posted')[:3]
    non_perishable_donations = donations.filter(is_perishable=False).order_by('-date_posted')[:3]

    context = {
        'perishable_donations': perishable_donations,
        'non_perishable_donations': non_perishable_donations,
        'perishable_food_donated': perishable_food_donated,
        'non_perishable_food_donated': non_perishable_food_donated,
        'food_pickups': food_pickups,
        'ngos_served': ngos_served,
        'num_restaurants_managed': num_restaurants_managed,
    }

    return render(request, 'donor/dashboard.html', context)



@requires_password_change
@login_required
def restaurants(request):
    restaurants = Restaurant.objects.filter(ManagerID=request.user)
    context = {'restaurants': restaurants}
    return render(request, 'donor/restaurants.html', context)


from django.shortcuts import render, redirect
from .forms import RestaurantCreationForm

@requires_password_change
@login_required
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantCreationForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.ManagerID = request.user
            restaurant.save()
            return redirect('donor:restaurants')
    else:
        form = RestaurantCreationForm()

    context = {'form': form}
    return render(request, 'donor/add_restaurant.html', context)

@requires_password_change
@login_required
def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    if request.method == 'POST':
        form = RestaurantCreationForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('donor:restaurants')
    else:
        form = RestaurantCreationForm(instance=restaurant)

    context = {'form': form}
    return render(request, 'donor/edit_restaurant.html', context)

@requires_password_change
@login_required
def restaurant_details(request, restaurant_id):
    # restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    restaurant = Restaurant.objects.annotate(avg_rating=Avg('restaurantrating__rating'), num_ratings=Count('restaurantrating__rating')).get(
        RestaurantID=restaurant_id)
    context = {'restaurant': restaurant}
    return render(request, 'donor/restaurant_details.html', context)


@requires_password_change
@login_required
def donate(request):
    top_organizations = Organization.objects.annotate(avg_rating=Avg('organizationrating__rating'),
                                                      num_ratings=Count('organizationrating__rating')).order_by('-avg_rating')[:5]
    other_organizations = Organization.objects.annotate(avg_rating=Avg('organizationrating__rating'),
                                                        num_ratings=Count('organizationrating__rating')).exclude(
        pk__in=top_organizations.values_list('pk', flat=True))

    return render(request, 'donor/donate_0.html',
                  {'top_organizations': top_organizations, 'other_organizations': other_organizations})

@requires_password_change
@login_required
def ngo_details(request, organization_id):
    organization = Organization.objects.annotate(avg_rating=Avg('organizationrating__rating'),
                                                 num_ratings=Count('organizationrating__rating')).get(
        OrganizationID=organization_id)
    return render(request, 'donor/ngo_details.html', {'organization': organization})

@requires_password_change
@login_required
def history(request):
    donor = request.user

    delivered_donations = Donation.objects.filter(RestaurantID__ManagerID=donor)
    perishable_donations = delivered_donations.filter(is_perishable=True, Status='delivered')
    non_perishable_donations = delivered_donations.filter(is_perishable=False, Status='delivered')

    context = {
        'perishable_donations': perishable_donations,
        'non_perishable_donations': non_perishable_donations,
    }

    return render(request, 'donor/history.html', context)

@requires_password_change
@login_required
def history_details(request, donation_id):
    donation = get_object_or_404(Donation, DonationID=donation_id)

    context = {
        'donation': donation,
    }

    return render(request, 'donor/history_details.html', context)



@requires_password_change
@require_POST
def store_pickup_code(request, donation_id):
    try:
        data = json.loads(request.body)
        pickup_code = data.get('pickup_code')

        if not pickup_code:
            return JsonResponse({'success': False, 'error': 'Missing pickup code'})

        donation = Donation.objects.get(pk=donation_id)
        if donation.is_accepted and donation.is_scheduled:
            donation.pickup_code = pickup_code
            donation.Status = 'Intransit'
            donation.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid donation status'})
    except Donation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Donation not found'})





from django.shortcuts import render, redirect
from donor.models import Organization, Restaurant
from .forms import DonationForm

@requires_password_change
@login_required
def make_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.user, request.POST)
        if form.is_valid():
            donation = form.save(commit=False)

            # Associate the organization with the donation
            organization = form.cleaned_data['OrganizationID']
            donation.Organization = organization

            donation.save()  # Save the donation record to the database

            if donation.is_perishable:
                return redirect('donor:perishable_donation_create', donation_id=donation.pk)
            else:
                return redirect('donor:non_perishable_donation_create', donation_id=donation.pk)
    else:
        form = DonationForm(request.user)

    return render(request, 'donor/donate_1.html', {'form': form})

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
            return redirect('donor:donations')

    return render(request, 'donor/perishable_donation_create.html',
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
            return redirect('donor:donations')

    return render(request, 'donor/non_perishable_donation_create.html',
                  {'donation': donation, 'non_perishable_donation_form': non_perishable_donation_form})

@requires_password_change
@login_required
def profile(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'donor/profile.html', context)

@requires_password_change
@login_required
def support(request):
    return render(request, 'donor/support.html')

@requires_password_change
@login_required
def raise_issue(request):
    return render(request, 'donor/raise_issue.html')


@requires_password_change
@login_required
def edit_profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.twitter_link = form.cleaned_data.get("twitter_link")
            user.instagram_link = form.cleaned_data.get("instagram_link")
            user.facebook_link = form.cleaned_data.get("facebook_link")
            user.save()
            return JsonResponse({"message": "Profile updated successfully"})
    else:
        form = ProfileForm(instance=user)

    context = {"form": form}
    return render(request, "donor/edit_profile.html", context)




@requires_password_change
@login_required
def about(request):
    return render(request, 'donor/about.html')

@requires_password_change
@login_required
def messaging(request):
    return render(request, 'donor/messaging.html')

@requires_password_change
@login_required
def send_message(request):
    return render(request, 'donor/send_message.html')

@requires_password_change
@login_required
def reply(request):
    return render(request, 'donor/reply.html')

@requires_password_change
@login_required
def notification(request):
    return render(request, 'donor/notification.html')

@requires_password_change
@login_required
def help_documentation(request):
    return render(request, 'donor/help_documentation.html')


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

    return render(request, 'donor/settings.html', context)

@requires_password_change
@login_required
def donations(request):
    call_command('cleardonations')

    user = request.user
    # Retrieve donations with ngo_requested=True and targeting the logged-in user's restaurants
    ngo_requested_donations = Donation.objects.filter(ngo_requested=True, RestaurantID__ManagerID=user,
                                                      is_accepted=False)
    # Retrieve accepted donations for the logged-in user's restaurants
    accepted_donations = Donation.objects.filter(
        Q(is_accepted=True, RestaurantID__ManagerID=user, Status='pending') |
        Q(is_accepted=True, RestaurantID__ManagerID=user, Status='Intransit')
    )
    # Retrieve posted donations for the logged-in user's restaurants
    posted_donations = Donation.objects.filter(
        Q(is_accepted=False, ngo_requested=False, RestaurantID__ManagerID=user, Status='pending') | Q(
            Organization__Name='all'))

    return render(request, 'donor/donations.html', {
        'ngo_requested_donations': ngo_requested_donations,
        'accepted_donations': accepted_donations,
        'posted_donations': posted_donations
    })

@requires_password_change
@login_required
def donation_details(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)

    return render(request, 'donor/donation_details.html', {'donation': donation})


from django.shortcuts import get_object_or_404

@requires_password_change
@login_required
def edit_donation(request, donation_id):
    donor = request.user
    try:
        donation = Donation.objects.get(pk=donation_id)
        if donation.RestaurantID.ManagerID != donor:
            return HttpResponseForbidden("You don't have permission to edit this donation.")
    except Donation.DoesNotExist:
        return HttpResponseNotFound("Donation not found.")

    perishable_donation = None
    non_perishable_donation = None
    donation_form = None

    if donation.is_perishable:
        try:
            perishable_donation = PerishableDonation.objects.get(Donation_id=donation_id)
            donation_form = PerishableDonationForm(request.POST or None, request.FILES or None,
                                                   instance=perishable_donation)
        except PerishableDonation.DoesNotExist:
            pass
    else:
        try:
            non_perishable_donation = NonPerishableDonation.objects.get(Donation_id=donation_id)
            donation_form = NonPerishableDonationForm(request.POST or None, request.FILES or None,
                                                      instance=non_perishable_donation)
        except NonPerishableDonation.DoesNotExist:
            pass

    if request.method == 'POST':
        if donation_form and donation_form.is_valid():
            donation_form.save()
            return redirect('donor:donations')

    return render(request, 'donor/edit_donation.html', {
        'donation_form': donation_form,
        'perishable_donation': perishable_donation,
        'non_perishable_donation': non_perishable_donation,
        'is_perishable': donation.is_perishable,
    })

@requires_password_change
@login_required
@require_POST
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
@login_required
@require_POST
def accept_donation(request, donation_id):
    try:
        with transaction.atomic():
            donation = get_object_or_404(Donation, pk=donation_id)
            donation.is_accepted = True
            donation.save()

            return JsonResponse({'success': True})
    except Donation.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Donation not found'})

@requires_password_change
@login_required
def my_donation_details(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)

    return render(request, 'donor/my_donation_details.html', {'donation': donation})

@requires_password_change
@login_required
def delete_restaurant(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        restaurant.delete()
        return JsonResponse({'success': True})
    except Restaurant.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Restaurant not found'})

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
        response['Content-Disposition'] = 'attachment; filename="donation_report.pdf"'

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
            ["Pickup Location", donation.perishabledonation.pickup_location if donation.is_perishable else donation.nonperishabledonation.MealTitle],
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
            "Thank you for your donation!",
            HexColor("#000000"),  # Hex code for black color
            "Terms and Conditions:",
            "- The donated goods should meet the required standards.",
            "- Any damages or discrepancies should be reported within 24 hours.",
            "- The donation is subject to acceptance by the receiving party.",
            "- Any unauthorized use or distribution is prohibited.",
        ]

        # Define the y-coordinate for the additional text
        y_additional_text = image_y - 400  # Adjust the y-coordinate

        for text in additional_text:
            if isinstance(text, str):
                p.setFont("Helvetica-Bold", 12)
                if text == "Thank you for your donation!":
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
from donor.models import Donation


@requires_password_change
@csrf_exempt
@require_POST
def rate_organization(request, donation_id):
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
            rating = OrganizationRating.objects.create(user=user, restaurant=restaurant, organization=organization,
                                           donation_id=donation_id,
                                           rated_entity_type='ORGANIZATION', rating=rating_value)
            rating.save()

            return JsonResponse({'message': 'Rating saved successfully.'})
        else:
            return JsonResponse({'message': 'Rating value is missing or invalid.'})
    else:
        return JsonResponse({'message': 'Restaurant or organization not found for the current user.'})


@requires_password_change
def check_rating_exists(request, donation_id):
    user = request.user
    try:
        donation = Donation.objects.get(pk=donation_id)

    except Donation.DoesNotExist:
        return JsonResponse({'exists': False})

    # Check if the rating exists for the current user and donation
    rating_exists = OrganizationRating.objects.filter(user=user, donation=donation).exists()
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
        html_content = render_to_string('donor/deletion_code_email.html', {'deletion_code': deletion_code})

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




