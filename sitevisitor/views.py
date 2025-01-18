from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from adminpanel.models import CustomUser, Job

from django.views.decorators.csrf import csrf_protect



def home(request):
    """
    Display all published jobs on the home page.
    If the user is not logged in, show a login prompt for applying.
    """
    jobs = Job.objects.all()  # Retrieve all jobs from the database
    return render(request, 'sitevisitor/home.html', {'jobs': jobs})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        print("Role Received:", role)  # Debugging Role
        form = CustomAuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            print("Authenticated User:", user, "Role:", user.role)  # Debugging User Role

            if role == 'recruiter' and user.is_recruiter:
                login(request, user)
                return redirect('jobs:jobs_home')
            elif role == 'candidate' and user.is_candidate:
                login(request, user)
                return redirect('users:users_home')
            else:
                messages.error(request, "Role mismatch: Your account does not match the selected role.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'sitevisitor/login.html', {'form': form})





def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'sitevisitor/register.html')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'sitevisitor/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use.")
            return render(request, 'sitevisitor/register.html')

        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('sitevisitor:login')

    return render(request, 'sitevisitor/register.html')








