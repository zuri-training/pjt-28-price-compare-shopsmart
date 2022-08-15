from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from smartshop import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "authenticate/index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect("signup")
            else:
                user = User.objects.create_user(username, email, pass1)
                user.is_active = False
                user.save()
                messages.success(request, "User created successfully. We have sent you an email with a link to verify your account.")

                # Welcome Email

                subject = "Welcome to SmartShop"
                message = "Hello" + username + "!! \n" + "Welcome to SmartShop!! \n \n" + "We hope you enjoy your shopping experience with us!! \n \n" + "We have also sent you a confirmation email, please confirm your email address to activate your account." + "Regards, \n" + "SmartShop Team"
                from_email = settings.EMAIL_HOST_USER
                to_list = [user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=True)

                # Email Confirmation

                current_site = get_current_site(request)
                email_subject = "Confirm your email address"
                message2 = render_to_string('email_confirmation.html', {
                    'name': user.name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                email = EmailMessage(
                    email_subject,
                    message2,
                    settings.EMAIL_HOST_USER
                    [user.email],
                )
                email.fail_silently = True
                email.send()

                return redirect("signin")
        else:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

    return render(request, "authenticate/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            name = username
            messages.success(request, "Login successful")
            return render(request, "authenticate/index.html", {'name': name})
        else:
            messages.error(request, "Invalid credentials")
            return redirect("home")

    return render(request, "authenticate/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("home")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')