from django.shortcuts import render


# Create your views here.

def dashboard(request):
    return render(request, 'donor/dashboard.html')


def restaurants(request):
    return render(request, 'donor/restaurants.html')


def add_restaurant(request):
    return render(request, 'donor/add_restaurant.html')


def edit_restaurant(request):
    return render(request, 'donor/edit_restaurant.html')


def donate(request):
    return render(request, 'donor/donate_0.html')


def ngo_details(request):
    return render(request, 'donor/ngo_details.html')


def history(request):
    return render(request, 'donor/history.html')


def history_details(request):
    return render(request, 'donor/history_details.html')


def make_donation(request):
    return render(request, 'donor/donate_1.html')


def profile(request):
    return render(request, 'donor/profile.html')


def support(request):
    return render(request, 'donor/support.html')


def raise_issue(request):
    return render(request, 'donor/raise_issue.html')


def edit_profile(request):
    return render(request, 'donor/edit_profile.html')


def change_password(request):
    return render(request, 'donor/change_password.html')


def about(request):
    return render(request, 'donor/about.html')


def messaging(request):
    return render(request, 'donor/messaging.html')


def send_message(request):
    return render(request, 'donor/send_message.html')


def reply(request):
    return render(request, 'donor/reply.html')


def notification(request):
    return render(request, 'donor/notification.html')


def help_documentation(request):
    return render(request, 'donor/help_documentation.html')


def settings(request):
    return render(request, 'donor/settings.html')


def donations(request):
    return render(request, 'donor/donations.html')


def donation_details(request):
    return render(request, 'donor/donation_details.html')


def edit_donation(request):
    return render(request, 'donor/edit_donation.html')


def my_donation_details(request):
    return render(request, 'donor/my_donation_details.html')
