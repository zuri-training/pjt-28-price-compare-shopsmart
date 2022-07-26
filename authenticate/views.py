import email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "authenticate/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if pass1 == pass2:
            if User.objects.filter(username).exists():
                messages.error(request, "Username already exists")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("signup")
            else:
                user = User.objects.create_user(username, email, pass1)
                user.name = username
                user.save()
                messages.success(request, "User created successfully")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

    return render(request, "authenticate/signup.html")

def login(request):

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            name = user.name
            messages.success(request, "Login successful")
            return render(request, "authenticate/index.html", {'name': name})
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home")

    return render(request, "authenticate/login.html")

def signout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("home")