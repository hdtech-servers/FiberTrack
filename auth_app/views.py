from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from .forms import CustomUserCreationForm, UserProfileForm

# User List (Admin Only)
@login_required(login_url='/auth_app/login/')
def user_list(request):
    # Fetch all users
    users = User.objects.all()

    # Handle Add User form submission
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()

    # Render the user list with the form
    return render(request, 'auth_app/user_list.html', {'users': users, 'form': form})

# Add User (Admin Only)
@login_required(login_url='/auth_app/login/')
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('user_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth_app/user_list.html', {'form': form})


# Edit User Profile (User)
@login_required(login_url='/auth_app/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'auth_app/edit_profile.html', {'form': form})

# View User Profile (User)
@login_required(login_url='/auth_app/login/')
def profile(request):
    return render(request, 'auth_app/profile.html')

# Change Password (User)
@login_required(login_url='/auth_app/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth_app/change_password.html', {'form': form})

# Delete User (Admin Only - Soft Delete Approach)
@login_required(login_url='/auth_app/login/')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = False  # Soft delete
        user.save()
        return redirect('user_list')
    return render(request, 'auth_app/confirm_delete.html', {'user': user})


# Custom Login View
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customer_list')  # Redirect to profile page after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth_app/login.html')


# Custom Logout View
@login_required(login_url='/auth_app/login/')
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

# Edit User (Admin)
@login_required(login_url='/auth_app/login/')
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'auth_app/edit_user.html', {'form': form, 'user': user})


@login_required(login_url='/auth_app/login/')
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'auth_app/user_detail.html', {'user': user})
