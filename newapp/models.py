from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    userobj = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    year = models.IntegerField()
    college = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    
    def __str__(self):
        return self.userobj.first_name + " " + self.userobj.last_name
    

# class Item(models.Model):
#     item = models.CharField(max_length=50)
#     price = models.FloatField()
    
#     def __str__(self):
#         return self.item + " " + str(self.price)
    
    
# Custom ManyToMany relationship between User and Item
class Order(models.Model):
    userobj = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    # itemobj = models.ForeignKey(Item, on_delete=models.CASCADE)
    orderdatetime = models.DateTimeField(auto_now_add=True)
    clothes = models.IntegerField()
    comfort = models.BooleanField()
    dettol = models.BooleanField()
    iron = models.IntegerField()
    bedspread = models.IntegerField()
    mediumblanket = models.IntegerField()
    largeblanket = models.IntegerField()
    totalprice = models.FloatField()
    status = models.CharField(max_length=15, default="Received")
    
    def __str__(self):
        return self.userobj.first_name + " " + self.userobj.last_name + " " + str(self.clothes) + " no.s" + " " + str(self.totalprice)


class CreditUser(models.Model):
    userobj = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    credit_left = models.FloatField(default=500)
    datetime = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField()
    
    def __str__(self):
        return self.userobj.first_name + " " + self.userobj.last_name
    

class YearlyUser(models.Model):
    userobj = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amt_left = models.FloatField(default=10000)
    datetime = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField()
    
    def __str__(self):
        return self.userobj.first_name + " " + self.userobj.last_name
    
    
class MonthlyUser(models.Model):
    userobj = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amt_left = models.FloatField(default=3000)
    datetime = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField()
    
    def __str__(self):
        return self.userobj.first_name + " " + self.userobj.last_name