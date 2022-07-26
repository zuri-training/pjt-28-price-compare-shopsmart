import email
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

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
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username, email=email, password=pass1)
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
        password = request.POST["password"]

        user = User.objects.filter(username=username)
        if user.exists():
            user = user.first()
            if user.check_password(password):
                messages.success(request, "Login successful")
                return redirect("home")
            else:
                messages.error(request, "Incorrect password")
                return redirect("login")
        else:
            messages.error(request, "Username does not exist")
            return redirect("login")

    return render(request, "authenticate/login.html")

def logout(request):
    pass