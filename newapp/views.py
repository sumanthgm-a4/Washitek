from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from newapp.models import *
from django.contrib.auth import logout, login, authenticate
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from random import randint


items = {
    "clothes": 40,
    "comfort": 5,
    "dettol": 10,
    "iron": 10,
    "bedspread": 40,
    "mediumblanket": 70,
    "largeblanket": 100,
}


# Create your views here.

def check_plan_expired(request):
    pass


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
    
    if request.user.is_staff:
        print("hello")
    
    return render(request, "index.html", {"uses_a_plan": get_plan(request)})


def render_about(request):
    
    return render(request, "about.html")


def render_services(request):
    
    return render(request, "service.html")


def render_pricing(request):
    
    return render(request, "pricing.html")


def render_credit(request):
    
    return render(request, "credit.html")


def render_elite_plus(request):
    
    return render(request, "elite_plus.html", {"uses_a_plan": get_plan(request)})


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
            recipient_list=['brijeshkhreddy@gmail.com'],
            fail_silently=False
        )
        messages.success(request, "Mail sent successfully")
        
    return render(request, "contact.html")


def render_login(request):
    
    if request.user.is_authenticated:
        messages.error(request, 'YOU LOGGED IN...')
        return redirect('home')
    
    if request.user.is_superuser:
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
                if user.is_superuser:
                    return redirect('/admin')
                messages.success(request, 'Logged in successfully')
                return redirect('home') 
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'User does not exist')

    return render(request, "login.html")


def render_reset_password(request):  
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        user = None
        if '@' in identifier:
            users = User.objects.filter(email=identifier)
            if users.exists():
                user = users[0]
        else:
            customers = Customer.objects.filter(mobile=identifier)
            if customers.exists():
                user = customers[0].userobj
        
        if user:
            send_otp(
                request=request,
                email=user.email,
                user_details={
                    'username': user.username
                } 
            )
            request.session['username'] = user.username
            messages.success(request, 'OTP sent successfully')
            return redirect('password_otp')
        else:
            messages.error(request, 'Invalid identifier')
            return render(request, "reset_pass.html")
    return render(request, "reset_pass.html")


def render_passwordotp(request):
    if request.method == "POST":
        otp = request.POST.get("otpfield")
        user = User.objects.get(username=request.session['username'])
        if request.session['otp'] == otp:
            request.session['otp_validated'] = True
            messages.success(request, 'OTP validated successfully')
            return redirect("change_password")
        messages.error(request, 'Invalid OTP')
        return redirect("password_otp")
    return render(request, "pass_otp.html")


def render_change_password(request):
    if not request.session.get('otp_validated'):
        return redirect('reset_password')
    if request.method == "POST":
        password = request.POST.get('passw')
        cpassword = request.POST.get('cpassw')
        if password == cpassword:
            user = User.objects.get(username=request.session['username'])
            user.set_password(password)
            user.save()
            request.session.clear()
            messages.success(request, 'Password changed successfully')
            return redirect('login')
        messages.error(request, 'Passwords do not match')
        return render(request, "change_pass.html")
    return render(request, "change_pass.html")


def render_logout(request):
    
    logout(request)
    messages.success(request, 'Logged out successfully')
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
        
        if len(passw) <= 8:
            messages.error(request, 'Password should be greater than 8 characters')
            return render(request, "signup.html")
        
        if not any(char in '!@#$%^&*()_+' for char in passw):
            messages.error(request, 'Password should contain at least one special character')
            return render(request, "signup.html")
        
        if not any(char.isdigit() for char in passw) or not any(char.isalpha() for char in passw):
            messages.error(request, 'Password should contain both alphabetic and numeric values')
            return render(request, "signup.html")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, "signup.html")
        
        if Customer.objects.filter(mobile=mobile).exists():
            messages.error(request, 'Mobile number already exists')
            return render(request, "signup.html")
        
        if passw != cpassw:
            messages.error(request, 'Passwords do not match')
            return render(request, "signup.html")
        
    
        send_otp(request=request, email=email, user_details={
                'fname': fname,
                'lname': lname,
                'gender': gender,
                'year': year,
                'cname': cname,
                'branch': branch,
                'mobile': mobile,
                'email': email,
                'passw': passw
            })
        return redirect("otp")
    else:
        return render(request, "signup.html")
    

def send_otp(request, email, user_details):
    otp = str(randint(100000, 999999))
    request.session['otp'] = otp
    request.session['user_details'] = user_details
    send_mail(from_email='sumanthgm12345@gmail.com', 
        subject=f"OTP for {email}", 
        message=otp, 
        recipient_list=[email], 
        fail_silently=False)
    return
    
    
def render_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp is None:
            messages.error(request, 'OTP is required')
            return render(request, "otp.html", {'error': 'OTP is required'})

        if entered_otp == request.session.get('otp'):
            user_details = request.session.get('user_details')
            try:
                user = User.objects.create_user(
                    username=user_details['email'],
                    password=user_details['passw'],
                    email=user_details['email'],
                    first_name=user_details['fname'],
                    last_name=user_details['lname'],
                    is_active=True
                )
                user.save()
                obj = Customer(
                    userobj=user,
                    gender=user_details['gender'],
                    year=user_details['year'],
                    college=user_details['cname'],
                    branch=user_details['branch'],
                    mobile=user_details['mobile']
                )
                obj.save()
                messages.success(request, 'User registered successfully')
                request.session.clear()
                return redirect("login")
            except IntegrityError:
                return render(request, "otp.html", {'error': 'An error occurred while creating the user'})
        else:
            messages.error(request, 'Invalid OTP')
            return render(request, "otp.html", {'error': 'Invalid OTP'})
    else:
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
    
    amt = None
    user = Customer.objects.get(userobj=request.user)
    if get_plan(request) == "Monthly Plan":
        planuser = MonthlyUser.objects.get(userobj=request.user)
        amt = planuser.amt_left
    elif get_plan(request) == "Yearly Plan":
        planuser = YearlyUser.objects.get(userobj=request.user)
        amt = planuser.amt_left
    elif get_plan(request) == "Credit Plan":
        planuser = CreditUser.objects.get(userobj=request.user)
        amt = planuser.credit_left
    else:
        amt = "N/A"
    
    return render(request, "profile.html", {"obj": user, "uses_a_plan": get_plan(request), "amt": amt})


def render_plan(request):
    
    if request.method == "POST":
        user = request.user
        plan = request.POST.get("plan")
        print(plan)
            
        if plan == "monthly":
            monthlyuser = MonthlyUser(userobj=user, isActive=True)
            monthlyuser.save()
            yearlyuser = YearlyUser(userobj=user, isActive=False)
            yearlyuser.save()
            credituser = CreditUser(userobj=user, isActive=False)
            credituser.save()
            messages.success(request, "Monthly plan activated")
            return redirect("home")
            
        if plan == "yearly":
            monthlyuser = MonthlyUser(userobj=user, isActive=False)
            monthlyuser.save()
            yearlyuser = YearlyUser(userobj=user, isActive=True)
            yearlyuser.save()
            credituser = CreditUser(userobj=user, isActive=False)
            credituser.save()
            messages.success(request, "Yearly plan activated")
            return redirect("home")
            
        if plan == "credit":
            monthlyuser = MonthlyUser(userobj=user, isActive=False)
            monthlyuser.save()
            yearlyuser = YearlyUser(userobj=user, isActive=False)
            yearlyuser.save()
            credituser = CreditUser(userobj=user, isActive=True)
            credituser.save()
            messages.success(request, "Credit plan activated")
            return redirect("home")
    
    return render(request, "plan.html", {"uses_a_plan": get_plan(request)})


@login_required(login_url="login")
def render_order(request):
    
    if request.method == "POST":
        clothes = int(request.POST.get("clothes", 0)) if request.POST.get("clothes") else 0
        comfort = int(request.POST.get("comfort")) if request.POST.get("comfort") else 0
        dettol = int(request.POST.get("dettol")) if request.POST.get("dettol") else 0
        iron = int(request.POST.get("iron"))
        bedspread = int(request.POST.get("bedspread"))
        mediumblanket = int(request.POST.get("mediumblanket"))
        largeblanket = int(request.POST.get("largeblanket"))
        
        print(clothes, comfort, dettol, iron, bedspread, mediumblanket, largeblanket)
        
        if clothes == 0 and comfort == 0 and dettol == 0 and iron == 0 and bedspread == 0 and mediumblanket == 0 and largeblanket == 0:
            messages.error(request, "Please select atleast one item")
            return redirect("order")
        
        if clothes == 0 and (comfort == 1 or dettol == 1):
            messages.error(request, "Comfort and Dettol can't be selected without clothes")
            return redirect("order")
        
        user = request.user
        totalprice = clothes*items["clothes"] + \
                        clothes*comfort*items["comfort"] + \
                        clothes*dettol*items["dettol"] + \
                        iron*items["iron"] + \
                        bedspread*items["bedspread"] + \
                        mediumblanket*items["mediumblanket"] + \
                        largeblanket*items["largeblanket"]
        
        order = Order(
            userobj=user, 
            clothes=clothes, 
            comfort=comfort, 
            dettol=dettol, 
            iron=iron, 
            bedspread=bedspread, 
            mediumblanket=mediumblanket, 
            largeblanket=largeblanket, 
            totalprice=totalprice
        )
        
        if YearlyUser.objects.filter(userobj=user).exists():
            if YearlyUser.objects.get(userobj=user).isActive:
                user = YearlyUser.objects.get(userobj=user)
                if user.amt_left < totalprice:
                    messages.error(request, "Insufficient balance")
                    return redirect("home")
                user.amt_left -= totalprice
                user.save()
                order.save()
                print(order.orderdatetime)
                messages.success(request, "Order placed successfully")
                return redirect("home")
            elif CreditUser.objects.get(userobj=user).isActive:
                user = CreditUser.objects.get(userobj=user)
                if user.credit_left < totalprice:
                    messages.error(request, "Insufficient credit")
                    return redirect("home")
                user.credit_left -= totalprice
                user.save()
                order.save()
                print(order.orderdatetime)
                messages.success(request, "Order placed successfully")
                return redirect("home")
            elif MonthlyUser.objects.get(userobj=user).isActive:
                user = MonthlyUser.objects.get(userobj=user)
                if user.amt_left < totalprice:
                    messages.error(request, "Insufficient balance")
                    return redirect("home")
                user.amt_left -= totalprice
                user.save()
                order.save()
                print(order.orderdatetime)
                messages.success(request, "Order placed successfully")
                return redirect("home")        
        else:
            messages.warning(request, "Please choose a plan")
            return redirect("plan")
    
    return render(request, "add_ones.html", {"uses_a_plan": get_plan(request)})


def check_price(request):
    if request.method == "POST":
        clothes = int(request.POST.get("clothes")) if request.POST.get("clothes") else 0
        comfort = int(request.POST.get("comfort")) if request.POST.get("comfort") else 0
        dettol = int(request.POST.get("dettol")) if request.POST.get("dettol") else 0
        iron = int(request.POST.get("iron"))
        bedspread = int(request.POST.get("bedspread"))
        mediumblanket = int(request.POST.get("mediumblanket"))
        largeblanket = int(request.POST.get("largeblanket"))
        
        print(clothes, comfort, dettol, iron, bedspread, mediumblanket, largeblanket)
        print("Hello")
        
        nonechosen = 0
        noclothes = 0
        
        if clothes == 0 and comfort == 0 and dettol == 0 and iron == 0 and bedspread == 0 and mediumblanket == 0 and largeblanket == 0:
            nonechosen = 1
            
        if clothes == 0 and (comfort == 1 or dettol == 1):
            noclothes = 1
        
        totalprice = clothes*items["clothes"] + \
                        clothes*comfort*items["comfort"] + \
                        clothes*dettol*items["dettol"] + \
                        iron*items["iron"] + \
                        bedspread*items["bedspread"] + \
                        mediumblanket*items["mediumblanket"] + \
                        largeblanket*items["largeblanket"]
                        
        return JsonResponse({"ordertotal": totalprice, "nonechosen": nonechosen, "noclothes": noclothes})


def render_view_orders(request):
    
    user = request.user
    orders = Order.objects.filter(userobj=user)[::-1]
    
    return render(request, "view_orders.html", {"orders": orders, "uses_a_plan": get_plan(request)})


def render_view_customers(request):
    
    customers = Customer.objects.all()
    
    return render(request, "view_customers.html", {"customers": customers, "uses_a_plan": get_plan(request)})


def render_customer_orders(request, cid):
    
    orders = Order.objects.filter(userobj=Customer.objects.get(id=cid).userobj)[::-1]
    
    return render(request, "customer_orders.html", {"orders": orders})


@csrf_exempt  # Exempt from CSRF if needed, or ensure CSRF token is passed
def update_order_status(request):
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')

        try:
            # Get the order and update its status
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()

            return JsonResponse({'message': 'Order status updated successfully!'})
        
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Order not found!'}, status=404)
        
    return JsonResponse({'message': 'Invalid request'}, status=400)


def render_download_data(request):
    
    orders = Order.objects.all()
    colleges = [i.userobj.customer.college for i in orders]
    colleges = list(set(colleges))
    colleges.append("All Colleges")
    print(colleges)
    
    if request.method == "POST":
        selected_value = request.POST.get('selected_value')
        print(selected_value)
        if selected_value == "All Colleges":
            orders = Order.objects.all()
        elif selected_value:
            orders = Order.objects.filter(userobj__customer__college=selected_value)
            print(orders)
        data = list(orders.values('id', 'userobj__first_name', 'userobj__last_name', 'userobj__email', 'userobj__customer__college', 'orderdatetime', 'clothes', 'status', 'totalprice'))
        return JsonResponse(data, safe=False)
    return render(request, "download_data.html", {"orders": orders, "colleges": colleges})