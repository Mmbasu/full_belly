from django.shortcuts import render


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


def drivers(request):
    return render(request, 'recipient/driver.html')


def edit_driver(request):
    return render(request, 'recipient/edit_driver.html')


def driver_details(request):
    return render(request, 'recipient/driver_details.html')


def add_driver(request):
    return render(request, 'recipient/add_driver.html')
