from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    userobj = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    year = models.IntegerField()
    college = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    
    def __str__(self):
        return self.userobj.username