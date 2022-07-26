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

        myuser = User.objects.create_user(username, email, pass1)
        myuser.name = username

        myuser.save()

        messages.success(request, "Your account has been created successfully")

        return redirect("login")

    return render(request, "authenticate/signup.html")

def login(request):
    return render(request, "authenticate/login.html")

def logout(request):
    pass