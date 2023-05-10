from django.shortcuts import render


# Create your views here.

def dashboard(request):
    return render(request, 'driver/dashboard.html')


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


def settings(request):
    return render(request, 'driver/settings.html')


def notification(request):
    return render(request, 'driver/notification.html')


def profile(request):
    return render(request, 'driver/profile.html')


def edit_profile(request):
    return render(request, 'driver/edit_profile.html')


def deliveries(request):
    return render(request, 'driver/deliveries.html')


def history(request):
    return render(request, 'driver/history.html')


def history_details(request):
    return render(request, 'driver/history_details.html')


def delivery_details(request):
    return render(request, 'driver/delivery_details.html')


def accepted_delivery_details(request):
    return render(request, 'driver/accepted_delivery_details.html')
