import json

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from reportlab.lib.colors import HexColor
from reportlab.platypus import TableStyle, Table

from donor.models import Donation
from driver.models import Delivery
from recipient.models import Driver, RecipientDelivery
from django.db import models
from django.contrib.auth.decorators import login_required

from .decorators import requires_password_change
from .forms import ChangePasswordForm, ProfileForm
from django.contrib.auth import update_session_auth_hash


from datetime import timedelta

@login_required
@requires_password_change
def dashboard(request):
    driver = request.user.driver
    delivered_deliveries = Delivery.objects.filter(DriverID=driver, Status='delivered')
    perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=True)
    non_perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=False)

    # Limiting donations to 3 and ordering by date_delivered in descending order
    perishable_deliveries = perishable_deliveries.order_by('-DonationID__date_delivered')[:3]
    non_perishable_deliveries = non_perishable_deliveries.order_by('-DonationID__date_delivered')[:3]

    # Calculate total time spent on road by the driver
    total_time_spent_on_road = timedelta(seconds=0)

    for delivery in delivered_deliveries:
        if delivery.DonationID.date_delivered and delivery.ActualPickupDateTime:
            time_spent = delivery.DonationID.date_delivered - delivery.ActualPickupDateTime
            total_time_spent_on_road += time_spent

    # Calculate the total number of pickups made by the driver
    total_pickups_made = delivered_deliveries.count()

    # Calculate the number of distinct restaurants served
    restaurants_served = delivered_deliveries.values('DonationID__RestaurantID').distinct().count()

    # Calculate hours and minutes for template display
    hours = total_time_spent_on_road.days * 24 + total_time_spent_on_road.seconds // 3600
    minutes = (total_time_spent_on_road.seconds // 60) % 60

    context = {
        'perishable_deliveries': perishable_deliveries,
        'non_perishable_deliveries': non_perishable_deliveries,
        'total_time_spent_on_road': total_time_spent_on_road,
        'total_pickups_made': total_pickups_made,
        'restaurants_served': restaurants_served,
        'hours': hours,
        'minutes': minutes,
    }
    return render(request, 'driver/dashboard.html', context)




@login_required
@requires_password_change
def support(request):
    return render(request, 'driver/support.html')

@login_required
@requires_password_change
def raise_issue(request):
    return render(request, 'driver/raise_issue.html')

@login_required
@requires_password_change
def messaging(request):
    return render(request, 'driver/messaging.html')

@login_required
@requires_password_change
def send_message(request):
    return render(request, 'driver/send_message.html')

@login_required
@requires_password_change
def reply(request):
    return render(request, 'driver/reply.html')

@login_required
@requires_password_change
def help_documentation(request):
    return render(request, 'driver/help_documentation.html')

@login_required
@requires_password_change
def about(request):
    return render(request, 'driver/about.html')


@login_required
def settings(request):
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
    return render(request, 'driver/settings.html', {'form': form})

@login_required
@requires_password_change
def notification(request):
    return render(request, 'driver/notification.html')


@login_required
@requires_password_change
def profile(request):
    user = request.user
    driver = Driver.objects.get(DriverID=user)

    context = {
        'user': user,
        'driver': driver,
    }
    return render(request, 'driver/profile.html', context)


@login_required
@requires_password_change
def edit_profile(request):
    user = request.user
    driver = Driver.objects.get(DriverID=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            # Update the corresponding Driver instance
            driver.first_name = form.cleaned_data['first_name']
            driver.last_name = form.cleaned_data['last_name']
            driver.photo = form.cleaned_data['photo']
            driver.phone = form.cleaned_data['phone']
            driver.save()

            # Update the corresponding User instance
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone = form.cleaned_data['phone']
            user.photo = form.cleaned_data['photo']
            user.twitter_link = form.cleaned_data.get("twitter_link")
            user.instagram_link = form.cleaned_data.get("instagram_link")
            user.facebook_link = form.cleaned_data.get("facebook_link")
            user.save()

            return JsonResponse({"message": "Profile updated successfully"})
        else:
            return JsonResponse({"error": "Invalid form data"}, status=400)
    else:
        form = ProfileForm(instance=user)

    context = {'form': form}
    return render(request, 'driver/edit_profile.html', context)




@login_required
@requires_password_change
def deliveries(request):
    try:
        driver = request.user.driver
        deliveries = Delivery.objects.filter(DriverID=driver)
    except Driver.DoesNotExist:
        # Handle the case when the logged-in user is not a driver or does not have a driver profile.
        deliveries = []

    context = {
        'deliveries': deliveries
    }
    return render(request, 'driver/deliveries.html', context)


@login_required
@requires_password_change
def history(request):
    driver = request.user.driver

    delivered_deliveries = Delivery.objects.filter(DriverID=driver, Status='delivered')
    perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=True, Status='delivered')
    non_perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=False, Status='delivered')

    context = {
        'delivered_deliveries': delivered_deliveries,
        'perishable_deliveries': perishable_deliveries,
        'non_perishable_deliveries': non_perishable_deliveries
    }
    return render(request, 'driver/history.html', context)

@login_required
@requires_password_change
def history_details(request, delivery_id):
    delivery = Delivery.objects.get(DeliveryID=delivery_id)
    donation = delivery.DonationID

    # Calculate hours and minutes
    time_spent = delivery.time_spent_on_road
    if time_spent:
        hours = time_spent.days * 24 + time_spent.seconds // 3600
        minutes = (time_spent.seconds // 60) % 60
    else:
        hours = None
        minutes = None

    context = {
        'delivery': delivery,
        'donation': donation,
        'hours': hours,
        'minutes': minutes,
    }

    return render(request, 'driver/history_details.html', context)


@login_required
@requires_password_change
def delivery_details(request, delivery_id):
    delivery = Delivery.objects.get(DeliveryID=delivery_id)

    context = {
        'delivery': delivery
    }
    return render(request, 'driver/delivery_details.html', context)

@login_required
@requires_password_change
def accepted_delivery_details(request):
    return render(request, 'driver/accepted_delivery_details.html')

@login_required
@requires_password_change
def logout_view(request):
    logout(request)
    return redirect('users:login')


from django.http import JsonResponse
from datetime import datetime, timedelta


@login_required
@requires_password_change
def update_actualpickupdatetime(request, delivery_id):
    if request.method == 'POST':
        current_datetime = datetime.now()

        delivery = Delivery.objects.get(DeliveryID=delivery_id)
        if delivery.ActualPickupDateTime:
            return JsonResponse({'success': False, 'error': 'Food has already been picked up.'})

        delivery.ActualPickupDateTime = current_datetime
        delivery.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


class DeliveryReportView(View):

    def get(self, request, delivery_id):
        # Fetch the delivery details based on the delivery_id
        delivery = Delivery.objects.get(DeliveryID=delivery_id)

        # Create a response object with PDF content type
        response = HttpResponse(content_type='application/pdf')

        # Set the filename for the downloaded PDF file
        response['Content-Disposition'] = 'attachment; filename="delivery_report.pdf"'

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
        p.drawString(250, image_y - 40, "Delivery Report")  # Adjust the y-coordinate for the text

        # Generate the PDF content with delivery details
        data = [
            ["ID", delivery.DeliveryID],
            ["Restaurant", delivery.DonationID.RestaurantID],
            ["NGO", delivery.DonationID.Organization],
            ["Meal",
             delivery.DonationID.perishabledonation.MealType if delivery.DonationID.is_perishable else delivery.DonationID.nonperishabledonation.MealTitle],
            ["Quantity",
             f"{delivery.DonationID.perishabledonation.MealQuantityPlates} Plates" if delivery.DonationID.is_perishable else f"{delivery.DonationID.nonperishabledonation.MealQuantityKgs} Kgs"],
            ["Food Type", "Perishable Food" if delivery.DonationID.is_perishable else "Non-Perishable Food"],
            ["Pickup Location", delivery.PickupPoint],
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
            "Thank you for your delivery!",
            HexColor("#000000"),  # Hex code for black color
            "Terms and Conditions:",
            "- The delivered goods should meet the required standards.",
            "- Any damages or discrepancies should be reported within 24 hours.",
            "- The delivery is subject to acceptance by the receiving party.",
            "- Any unauthorized use or distribution is prohibited.",
        ]

        # Define the y-coordinate for the additional text
        y_additional_text = image_y - 400  # Adjust the y-coordinate

        for text in additional_text:
            if isinstance(text, str):
                p.setFont("Helvetica-Bold", 12)
                if text == "Thank you for your delivery!":
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


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone

@require_POST
@requires_password_change
def validate_pickup_code(request, donation_id):
    data = json.loads(request.body)
    pickup_code = data.get('pickup_code')

    if not pickup_code:
        return JsonResponse({'success': False, 'error': 'Missing pickup code'})

    donation = get_object_or_404(Donation, pk=donation_id)

    if donation.pickup_code == pickup_code:
        # Update donation status to "Intransit" and save it
        donation.Status = "Intransit"
        donation.save()

        # Update related models' status fields
        with transaction.atomic():
            recipient_delivery = RecipientDelivery.objects.get(DonationID=donation)
            recipient_delivery.Status = "Intransit"
            recipient_delivery.save()

            delivery = Delivery.objects.get(DonationID=donation)
            delivery.Status = "Intransit"
            delivery.ActualPickupDateTime = timezone.now()  # Record actual pickup date
            delivery.save()

            # Update driver status to "onDelivery"
            driver = donation.driver
            driver.Status = "onDelivery"
            driver.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid pickup code'})


