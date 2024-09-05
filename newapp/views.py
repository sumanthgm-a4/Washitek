from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from newapp.models import *
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.utils import IntegrityError

# Create your views here.
def render_home(request):
    
    return render(request, "index.html")


def render_about(request):
    
    return render(request, "about.html")


def render_services(request):
    
    return render(request, "service.html")


def render_pricing(request):
    
    return render(request, "pricing.html")


def render_use_and_pay(request):
    
    return render(request, "use_and_pay.html")


def render_elite_plus(request):
    
    return render(request, "elite_plus.html")


def render_contact(request):
    
    if request.method == "POST":
        firstname  = request.POST.get("first-name")
        lastname = request.POST.get("last-name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        message = request.POST.get("message")
        send_mail(
            from_email=email, 
            subject=f"Mail from {firstname} {lastname} - {email}",
            message=message,
            recipient_list=['sumanthgm12345@gmail.com'],
            fail_silently=False
        )
        messages.success(request, "Mail sent successfully")
        
    return render(request, "contact.html")


def render_login(request):
    if request.user.is_authenticated:
        messages.error(request, 'YOU LOGGED IN...')
        return redirect('home')
    
    if request.method == 'POST':
        identifier = request.POST['identifier']
        password = request.POST['passw']
        print(f"Identifier: {identifier}")
        print(f"Password: {password}")
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
                username = user.username
            except User.DoesNotExist:
                username = None
        else:
            try:
                customer = Customer.objects.get(mobile=identifier)
                username = customer.userobj.username
            except Customer.DoesNotExist:
                username = None

        if username:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid identifier')

    return render(request, "login.html")


def render_logout(request):
    
    logout(request)
    return redirect("login")


def render_register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        gender = request.POST['gender']
        year = request.POST['year']
        cname = request.POST['cname']
        branch = request.POST['branch']
        mobile = request.POST['mobile']
        email = request.POST['email']
        passw = request.POST['passw']
        cpassw = request.POST['cpassw']

        if passw == cpassw:
            if User.objects.filter(username=fname).exists():
                return render(request, "signup.html", {'error': 'Username already exists'})
            try:
                user = User.objects.create_user(username=fname, password=passw, email=email, first_name=fname, last_name=lname)
                user.save()
                obj = Customer(userobj=user, gender=gender, year=year, college=cname, branch=branch, mobile=mobile)
                obj.save()
                return redirect("login")  
            except IntegrityError:
                return render(request, "signup.html", {'error': 'An error occurred while creating the user'})
        else:
            return render(request, "signup.html", {'error': 'Passwords do not match'})
    else:
        return render(request, "signup.html")


def render_free_pickup(request):
    
    return render(request, "Free_pick_up.html")



def render_free_pickup(request):
    
    return render(request, "Free_pick_up.html")


def render_wash_and_dry(request):
    
    return render(request, "Wash_and_Dry.html")


def render_fold_and_iron(request):
    
    return render(request, "Fold_and_Iron.html")


def render_free_delivery(request):
    
    return render(request, "Free_Delivery.html")


@login_required(login_url="login")
def render_profile(request):
    
    obj = None
    if Customer.objects.filter(userobj=request.user).exists():
        obj = Customer.objects.get(userobj=request.user)
    return render(request, "profile.html", {"obj": obj})