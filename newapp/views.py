from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from newapp.models import *

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
    
    return render(request, "contact.html")


def render_login(request):
    
    return render(request, "login.html")


def render_register(request):
    
    return render(request, "signup.html")


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