from django.urls import path
from newapp.views import *

urlpatterns = [
    path("", render_home, name="home"),
    path("about", render_about, name="about"),
    path("services", render_services, name="services"),
    path("pricing", render_pricing, name="pricing"),
    path("contact", render_contact, name="contact"),
    path("login", render_login, name="login"),
    path("register", render_register, name="register"),
    path("freepickup", render_free_pickup, name="free_pickup"),
    path("washanddry", render_wash_and_dry, name="wash_and_dry"),
    path("foldandiron", render_fold_and_iron, name="fold_and_iron"),
    path("freedelivery", render_free_delivery, name="free_delivery"),
    path("profile", render_profile, name="profile"),
    path("useandpay", render_use_and_pay, name="use_and_pay"),
    path("eliteplus", render_elite_plus, name="elite_plus"),
    path("logout", render_logout, name="logout"),
]