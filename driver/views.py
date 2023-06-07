from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from driver.models import Delivery
from recipient.models import Driver, RecipientDelivery
from django.db import models



def dashboard(request):
    delivered_deliveries = RecipientDelivery.objects.filter(Status='delivered')
    perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=True)
    non_perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=False)
    distance_travelled = Delivery.objects.aggregate(models.Sum('DistanceTraveled'))['DistanceTraveled__sum']
    time_spent_on_road = Delivery.objects.aggregate(models.Sum('TimeSpentOnRoad'))['TimeSpentOnRoad__sum']
    deliveries_made = Delivery.get_deliveries_made()

    context = {
        'delivered_deliveries': delivered_deliveries,
        'perishable_deliveries': perishable_deliveries,
        'non_perishable_deliveries': non_perishable_deliveries,
        'distance_travelled': distance_travelled,
        'time_spent_on_road': time_spent_on_road,
        'deliveries_made': deliveries_made,
    }
    return render(request, 'driver/dashboard.html', context)


def support(request):
    return render(request, 'driver/support.html')


def raise_issue(request):
    return render(request, 'driver/raise_issue.html')


def messaging(request):
    return render(request, 'driver/messaging.html')


def send_message(request):
    return render(request, 'driver/send_message.html')


def reply(request):
    return render(request, 'driver/reply.html')


def help_documentation(request):
    return render(request, 'driver/help_documentation.html')


def about(request):
    return render(request, 'driver/about.html')


from django.contrib.auth.decorators import login_required
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash

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




def notification(request):
    return render(request, 'driver/notification.html')


from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    user = request.user
    driver = Driver.objects.get(
        DriverID=user)  # Assuming there is a one-to-one relationship between CustomUser and Driver models

    context = {
        'user': user,
        'driver': driver,
    }
    return render(request, 'driver/profile.html', context)


def edit_profile(request):
    return render(request, 'driver/edit_profile.html')


def deliveries(request):
    not_accepted_deliveries = Delivery.objects.filter(AcceptedDelivery=False)
    accepted_deliveries = Delivery.objects.filter(AcceptedDelivery=True)

    context = {
        'not_accepted_deliveries': not_accepted_deliveries,
        'accepted_deliveries': accepted_deliveries,
    }
    return render(request, 'driver/deliveries.html', context)



def history(request):
    delivered_deliveries = RecipientDelivery.objects.filter(Status='delivered')
    perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=True)
    non_perishable_deliveries = delivered_deliveries.filter(DonationID__is_perishable=False)
    context = {
        'delivered_deliveries': delivered_deliveries,
        'perishable_deliveries': perishable_deliveries,
        'non_perishable_deliveries': non_perishable_deliveries
    }
    return render(request, 'driver/history.html', context)


def history_details(request, delivery_id):
    delivery = Delivery.objects.get(DeliveryID=delivery_id)
    donation = delivery.DonationID

    context = {
        'delivery': delivery,
        'donation': donation,
    }

    return render(request, 'driver/history_details.html', context)


def delivery_details(request):
    return render(request, 'driver/delivery_details.html')


def accepted_delivery_details(request):
    return render(request, 'driver/accepted_delivery_details.html')


def logout_view(request):
    logout(request)
    return redirect('users:login')
