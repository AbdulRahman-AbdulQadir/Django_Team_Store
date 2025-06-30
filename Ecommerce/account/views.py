from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm, UserProfileForm, ChangePasswordForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from Products.models import Customer
# Create your views here.

def login_user(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            context['error'] = "Both fields are required."
        else:  
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("You Have Been Logged In!"))
                return redirect('home')
            else:
                context['error'] = "Invalid username or password."
        context['username'] = username
    return render(request, 'account/login.html', context)
def logout_user(request):
    logout(request)
    return render(request, 'account/logout.html', {})
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'You have registered successfully! Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'account/register.html', {'form': form})
@login_required
def user_profile(request):
    edit_mode = request.GET.get('edit') == 'true' # Check if 'edit' parameter is explicitly 'true'

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            edit_mode = True 

    else:
        form = UserProfileForm(instance=request.user)
    current_full_name = f"{request.user.first_name} {request.user.last_name}".strip()
    current_email = request.user.email
    current_username = request.user.username
    try:
        profile = request.user.customer
        phone = profile.phone
    except Customer.DoesNotExist:
        phone = None

    context = {
        # …same as before…
        'current_phone_number': phone,
    }
    context = {
        'form': form,
        'edit_mode': edit_mode,
        'current_full_name': current_full_name,
        'current_email': current_email,
        'current_username': current_username,
        'current_phone_number': phone,
    }
    return render(request, 'account/user_profile.html', context)
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                user = form.save()
                # IMPORTANT: Updates the user's session hash to prevent them from being logged out
                # due to the password change.
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('home') # Or wherever you want to redirect after success
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ChangePasswordForm(current_user)

        return render(request, 'account/update_password.html', {'form': form})
    else:
        # If the user is not authenticated, redirect them to the login page
        messages.warning(request, 'You must be logged in to change your password.')
        return redirect('login') # Assuming 'login' is your login URL name