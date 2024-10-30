from django.contrib import admin
from newapp.models import *

# Register your models here.

admin.site.register(Customer)
# admin.site.register(CreditUser)
# admin.site.register(Item)
admin.site.register(Order)
admin.site.register(YearlyUser)
admin.site.register(MonthlyUser)