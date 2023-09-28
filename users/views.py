from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import logout


from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import CustomAuthenticationForm, CustomUserCreationForm, CustomPasswordResetForm, MySetPasswordForm
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import uuid
from django.urls import reverse
from .models import CustomUser
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
import json


# @ensure_csrf_cookie
# def login(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             form = CustomAuthenticationForm(data=data)
#             username = form.data.get('username')
#             password = form.data.get('password')
#             try:
#                 user = CustomUser.objects.get(username=username)
#                 if not user.is_active:
#                     return JsonResponse({'success': False, 'errors': {'__all__': [form.error_messages['inactive']]}})
#             except CustomUser.DoesNotExist:
#                 pass
#             user = authenticate(request=request, username=username, password=password)
#             if user is not None:
#                 if form.is_valid():
#                     auth_login(request, user)
#                     return JsonResponse({'success': True})
#                 else:
#                     return JsonResponse(
#                         {'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
#             else:
#                 return JsonResponse({'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
#         except json.decoder.JSONDecodeError:
#             return JsonResponse({'success': False, 'errors': {'all': ['Invalid data format']}})
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})


# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login as auth_login
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.urls import reverse
#
# @ensure_csrf_cookie
# def login(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             form = CustomAuthenticationForm(data=data)
#             username = form.data.get('username')
#             password = form.data.get('password')
#             try:
#                 user = CustomUser.objects.get(username=username)
#                 if not user.is_active:
#                     return JsonResponse({'success': False, 'errors': {'__all__': [form.error_messages['inactive']]}})
#             except CustomUser.DoesNotExist:
#                 pass
#             user = authenticate(request=request, username=username, password=password)
#             if user is not None:
#                 if form.is_valid():
#                     auth_login(request, user)
#                     return JsonResponse({'success': True, 'redirect_url': get_dashboard_url(user.role)})
#                 else:
#                     return JsonResponse({'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
#             else:
#                 return JsonResponse({'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
#         except json.decoder.JSONDecodeError:
#             return JsonResponse({'success': False, 'errors': {'all': ['Invalid data format']}})
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'users/login.html', {'form': form})

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
import json
from django.utils import timezone
from .models import CustomUser  # Import your CustomUser model

@ensure_csrf_cookie
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = CustomAuthenticationForm(data=data)
            username = form.data.get('username')
            password = form.data.get('password')

            # Check if login attempts exceeded
            try:
                user = CustomUser.objects.get(username=username)
                if user.failed_login_attempts >= 3:
                    if user.last_login_attempt_exceeded is None:
                        user.last_login_attempt_exceeded = timezone.now()
                        user.save()
                    if user.last_login_attempt_exceeded is not None:  # Check if it's not None
                        # Check if it's been more than 1 minute since the last attempt exceeded
                        if (timezone.now() - user.last_login_attempt_exceeded).total_seconds() < 60:
                            return JsonResponse({'success': False, 'disable_login_button': True,
                                                 'errors': {'__all__': [form.error_messages['invalid_login_attempts']]}})
                        else:
                            # Reset failed login attempts if more than 1 minute has passed
                            user.failed_login_attempts = 0
                            user.last_login_attempt_exceeded = None
                            user.save()

            except CustomUser.DoesNotExist:
                pass

            user = authenticate(request=request, username=username, password=password)

            if user is not None:
                if form.is_valid():
                    auth_login(request, user)
                    # Reset the failed login attempts count and timestamp on successful login
                    user.failed_login_attempts = 0
                    user.last_login_attempt_exceeded = None
                    user.save()
                    return JsonResponse({'success': True, 'redirect_url': get_dashboard_url(user.role)})
                else:
                    return JsonResponse(
                        {'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
            else:
                # Authentication failed, increment failed login attempts
                try:
                    user = CustomUser.objects.get(username=username)
                    if not user.is_active:
                        return JsonResponse(
                            {'success': False, 'errors': {'__all__': [form.error_messages['inactive']]}})

                    # Increment failed login attempts if it's less than 3
                    user.failed_login_attempts += 1
                    user.save()
                    return JsonResponse(
                        {'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
                except CustomUser.DoesNotExist:
                    return JsonResponse(
                        {'success': False, 'errors': {'__all__': [form.error_messages['invalid_login']]}})
        except json.decoder.JSONDecodeError:
            return JsonResponse({'success': False, 'errors': {'all': ['Invalid data format']}})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})




def get_dashboard_url(role):
    if role == 'driver':
        return reverse('driver:dashboard')
    elif role == 'donor':
        return reverse('donor:dashboard')
    elif role == 'recipient':
        return reverse('recipient:dashboard')
    else:
        return reverse('recipient:dashboard')  # Replace with your default dashboard URL



def register(request):
    if request.method == 'POST':
        try:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.activation_token = str(uuid.uuid4())
                user.role = form.cleaned_data['role']  # Use form.cleaned_data to access the cleaned data
                user.save()

                # Send the activation email
                subject = 'Activate your Account'
                activate_url = request.build_absolute_uri(reverse('users:activate_account',
                                                                  args=[urlsafe_base64_encode(force_bytes(user.pk)),
                                                                        user.activation_token]))
                context = {'token': user.activation_token, 'activate_url': activate_url, 'user': user}
                html_content = render_to_string('users/activation.html', context)
                msg = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, [user.email])
                msg.content_subtype = 'html'
                msg.send(fail_silently=True)

                return JsonResponse({'success': True})
            else:
                errors = form.errors
                return JsonResponse({'success': False, 'errors': errors})
        except Exception as e:
            return JsonResponse({'success': False, 'errors': {'__all__': ['Something went wrong. Please try again.']}})
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})



def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid, activation_token=token)
        user.is_active = True
        user.activation_token = None
        user.save()

        # Send the welcome email
        subject = "Hello There Friend!"

        # Render the HTML template
        html_content = render_to_string('users/welcome_email.html', {'user': user})

        # Create the email message
        msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [user.email])
        msg.attach_alternative(html_content, "text/html")

        # Send the email
        msg.send(fail_silently=True)

        return redirect('users:login')
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, 'users/activation_error.html')


import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

def forgot_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        form = CustomPasswordResetForm({'email': email})
        if form.is_valid():
            try:
                user = CustomUser.objects.get(email=email)
                # Generate a random secure password
                new_password = CustomUser.objects.make_random_password()

                # Update user's password and save,
                user.set_password(new_password)
                user.temporary_password = new_password  # Set the temporary password field
                user.save()

                # Send email with the new password and instructions
                subject = 'Password Reset'
                html_content = render_to_string('users/password_reset_email.html', {'new_password': new_password})

                msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [email])
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)

                return JsonResponse({'success': True})
            except CustomUser.DoesNotExist:
                return JsonResponse({'success': True})
        else:
            errors = {}
            for field_name, field_errors in form.errors.items():
                errors[field_name] = field_errors[0]
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = CustomPasswordResetForm()

    return render(request, 'users/forgot_password.html', {'form': form})





#
# def forgot_password(request):
#     if request.method == 'POST':
#         # Get the raw JSON payload
#         json_data = request.body.decode('utf-8')
#         data = json.loads(json_data)
#
#         form = CustomPasswordResetForm(data)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             user = CustomUser.objects.filter(email=email).first()
#             if user is not None:
#                 # Generate a unique token
#                 token = user.generate_password_reset_token()
#
#                 # Build the password reset URL
#                 uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#                 password_reset_url = reverse('users:my_password_reset_confirm',
#                                              kwargs={'uidb64': uidb64, 'token': token})
#                 reset_url = request.build_absolute_uri(password_reset_url)
#
#                 # Send the password reset email
#                 subject = 'Reset Your Password'
#                 context = {'user': user, 'reset_url': reset_url}
#                 html_content = render_to_string('users/reset_password_email.html', context)
#                 msg = EmailMultiAlternatives(subject, html_content, 'admin@example.com', [email])
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()
#
#                 return JsonResponse({'success': True})
#             else:
#                 # Email doesn't exist in the system
#                 return JsonResponse({'success': False, 'errors': {'email': ['Email not found in the system']}})
#         else:
#             # Form is not valid
#             return JsonResponse({'success': False, 'errors': form.errors})
#
#     else:
#         form = CustomPasswordResetForm()
#         return render(request, 'users/forgot_password.html', {'form': form})
#
#
# def my_password_reset_confirm(request, uidb64, token):
#     """
#     View that handles the password reset confirm link.
#     """
#     User = get_user_model()
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
#         user = None
#
#     if user is None:
#         # Invalid user ID
#         print('Invalid User ID')
#         return HttpResponseBadRequest('Invalid User ID')
#
#     # if not user.is_password_reset_token_valid(token):
#     #     # Invalid token
#     #     print('Invalid token')
#     #     return HttpResponseBadRequest('Invalid token')
#
#     if user.password_reset_token and user.password_reset_used:
#         # Password reset link has already been used
#         print('Password reset link has already been used')
#         return HttpResponseBadRequest('Password reset link has already been used')
#
#     if request.method == 'POST':
#         form = MySetPasswordForm(user, request.POST)
#         if form.is_valid():
#             # Set the new password for the user
#             user.set_password(form.cleaned_data['new_password1'])
#             if user.password_reset_token:
#                 user.password_reset_used = True
#                 # user.password_reset_used.save()
#             user.save()
#             # Log the user in
#             user = authenticate(
#                 username=user.username,
#                 password=form.cleaned_data['new_password1']
#             )
#             login(request, user)
#
#             return render(request, 'registration/password_reset_email.html')
#         else:
#             return render(request, 'registration/password_reset_confirm.html', {'form': form})
#     else:
#         form = MySetPasswordForm(user)
#         return render(request, 'registration/password_reset_confirm.html', {'form': form})


def landing(request):
    return render(request, 'users/landing.html')

from django.http import JsonResponse
from django.shortcuts import render
from .forms import NewsletterSubscriptionForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@ensure_csrf_cookie
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)

        if form.is_valid():
            # Process the valid form data, e.g., save to the database
            # Replace this with your actual logic
            email = form.cleaned_data['email']
            # Save or process the email as needed

            # Sending the email
            subject = 'Full Belly Project Newsletter'

            # Render the HTML template
            html_content = render_to_string('users/news_welcome_email.html')

            # Create the email message
            msg = EmailMultiAlternatives(subject, '', settings.EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")

            # Send the email
            try:
                msg.send(fail_silently=True)
            except Exception as e:
                return JsonResponse({'success': False, 'errors': {'email': str(e)}})

            # Return a success JSON response
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with form errors
            errors = form.errors
            return JsonResponse({'errors': errors})

    return render(request, 'landing.html', {'form': NewsletterSubscriptionForm()})


from django.http import JsonResponse
from django.contrib.auth import authenticate

def check_login_button_status(request):
    if request.method == 'POST':
        # Extract username and password from the request POST data
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Attempt authentication with provided username and password
        user = authenticate(request=request, username=username, password=password)

        if user is not None and hasattr(user, 'failed_login_attempts'):
            if user.failed_login_attempts >= 3:
                return JsonResponse({'disable_login_button': True})

    return JsonResponse({'disable_login_button': False})



