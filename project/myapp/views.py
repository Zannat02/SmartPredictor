from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .models import House


def home(request):
    return render(request, 'home.html')
   
def login(request):
    if request.method == 'POST':
        username = request.POST.get("u_name")
        password = request.POST.get("u_password")
        
        authenticated_user = authenticate(request, username=username, password=password)

        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, f"Welcome, {username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        u_name = request.POST.get("u_name")
        u_fname = request.POST.get("u_fname")
        u_lname = request.POST.get("u_lname")
        u_email = request.POST.get("u_email")
        u_password = request.POST.get("u_password")
        u_age = request.POST.get("u_age")
        u_address = request.POST.get("u_address")
        u_mobile = request.POST.get("u_mobile")
        u_gender = request.POST.get("u_gender")

        if User.objects.filter(username=u_name).exists() or User.objects.filter(email=u_email).exists():
            messages.error(request, "Username or email already exists.")
            return redirect("register")

        user = User.objects.create_user(username=u_name, first_name=u_fname, last_name=u_lname, email=u_email, password=u_password)
        
        if user:
            user_profile = UserProfile(user=user, age=u_age, address=u_address, mobile=u_mobile, gender=u_gender)
            user_profile.save()
            authenticated_user = authenticate(request, username=u_name, password=u_password)

            if authenticated_user is not None:
                auth_login(request, authenticated_user) 
                messages.success(request, "Your account has been successfully created.")
                return redirect("home")
        
        messages.error(request, "User registration failed. Please try again.")
        return redirect("register") 
            
    return render(request, 'register.html')

def user_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'user_profile.html', context)


@login_required
def logout(request):
    user = request.user
    auth_logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('home')

def houses(request):
    houses = House.objects.all()
    return render(request, 'houses.html', {'houses': houses})

def prediction(request):
    return render(request, 'prediction.html')

def about_us(request):
    return render(request, 'about_us.html')
