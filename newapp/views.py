from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from newapp.models import *
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.utils import IntegrityError
from random import randint


# items = {
#     "comfort extra": 5,
#     "dettol extra": 10,
#     "iron": 10,
#     "bed spread": 40,
#     "medium blanket": 70,
#     "large blanket": 100,
# }


# Create your views here.

def get_plan(request):
    
    user= request.user
    uses_a_plan = None
    if user.is_authenticated and MonthlyUser.objects.filter(userobj=user).exists():
        if MonthlyUser.objects.get(userobj=user).isActive:
            uses_a_plan = "Monthly Plan"
        elif YearlyUser.objects.get(userobj=user).isActive:
            uses_a_plan = "Yearly Plan"
        elif CreditUser.objects.get(userobj=user).isActive:
            uses_a_plan = "Credit Plan"
            
    return uses_a_plan
    
def render_home(request):
    
    return render(request, "index.html", {"uses_a_plan": get_plan(request)})


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
    
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin')
    
    if request.method == 'POST':
        username = None
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
        elif identifier.isdigit():
            try:
                customer = Customer.objects.get(mobile=identifier)
                username = customer.userobj.username
            except Customer.DoesNotExist:
                username = None
        elif User.objects.filter(username=identifier).exists():
            username = identifier

        if username:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser or user.is_staff:
                    return redirect('/admin')
                return redirect('home') 
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid identifier')

    return render(request, "login.html")


def render_reset_password(request):
    pass    
#     if request.method == 'POST':
#         identifier = request.POST.get('identifier')
#         user = None
#         if '@' in identifier:
#             user = User.objects.filter(email=identifier)[0]
#         else:
#             user = Customer.objects.filter(mobile=identifier)[0].userobj
#         if user:
#             send_otp(
#                 request=request,
#                 email=user.email,
#                 username=user.username
#             )
#             return redirect('otp')
#         messages.error(request, 'Invalid identifier')
#         return render(request, "reset_pass.html")
    
#     return render(request, "reset_pass.html")


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

        if len(mobile) != 10:
            messages.error(request, 'Mobile number should be 10 digits')
            return render(request, "signup.html")
        
        if passw == cpassw:
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email already exists')
                return render(request, "signup.html")
            elif Customer.objects.filter(mobile=mobile).exists():
                messages.error(request, 'Mobile number already exists')
                return render(request, "signup.html")
            
            try:
                user = User.objects.create_user(username=email, password=passw, email=email, first_name=fname, last_name=lname, is_active=False)
                user.save()
                obj = Customer(userobj=user, gender=gender, year=year, college=cname, branch=branch, mobile=mobile)
                obj.save()
                send_otp(request=request, email=email, username=user.username)
                return redirect("otp")  
            except IntegrityError:
                return render(request, "signup.html", {'error': 'An error occurred while creating the user'})
        else:
            messages.error(request, 'Passwords do not match')
            return render(request, "signup.html", {'error': 'Passwords do not match'})
    else:
        return render(request, "signup.html")
    

def send_otp(request, email, username):
    otp = str(randint(100000, 999999))
    request.session['otp'] = otp
    request.session['username'] = username
    print(request.session['username'], request.session['otp'])
    send_mail(from_email='sumanthgm12345@gmail.com', 
        subject=f"OTP for {email}", 
        message=otp, 
        recipient_list=[email], 
        fail_silently=False)
    return
    
    
def render_otp(request):
    
    if request.method == "POST":
        otp = request.POST.get("otpfield")
        print(otp)
        print(request.session['username'])
        user = User.objects.get(username=request.session['username'])
        print(user)
        if request.session['otp'] == otp:
            print("Yes")
            user.is_active = True
            user.save()
            request.session.clear()
            messages.success(request, 'User created successfully')
            return redirect("login")
        messages.error(request, 'Invalid OTP')
        return redirect("otp")
    return render(request, "otp.html")


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
    
    user = Customer.objects.get(userobj=request.user)
    
    return render(request, "profile.html", {"obj": user, "uses_a_plan": get_plan(request)})


def render_plan(request):
    
    if request.method == "POST":
        user = request.user
        plan = request.POST.get("plan")
        print(plan)
            
        if plan == "monthly":
            monthlyuser = MonthlyUser(userobj=user, comf_dettol=False, isActive=True)
            monthlyuser.save()
            yearlyuser = YearlyUser(userobj=user, comf_dettol=False, isActive=False)
            yearlyuser.save()
            credituser = CreditUser(userobj=user, isActive=False)
            credituser.save()
            messages.success(request, "Monthly plan activated")
            return redirect("home")
            
        if plan == "yearly":
            monthlyuser = MonthlyUser(userobj=user, comf_dettol=False, isActive=False)
            monthlyuser.save()
            yearlyuser = YearlyUser(userobj=user, comf_dettol=False, isActive=True)
            yearlyuser.save()
            credituser = CreditUser(userobj=user, isActive=False)
            credituser.save()
            messages.success(request, "Yearly plan activated")
            return redirect("home")
            
        if plan == "credit":
            monthlyuser = MonthlyUser(userobj=user, comf_dettol=False, isActive=False)
            monthlyuser.save()
            yearlyuser = YearlyUser(userobj=user, comf_dettol=False, isActive=False)
            yearlyuser.save()
            credituser = CreditUser(userobj=user, isActive=True)
            credituser.save()
            messages.success(request, "Credit plan activated")
            return redirect("home")
    
    return render(request, "plan.html", {"uses_a_plan": get_plan(request)})