
from django.db.models import CASCADE

from django.db import models
from django.contrib.auth.models import AbstractUser

class Branch(models.Model):
    name=models.CharField(max_length=100)

class Product(models.Model):
    name=models.CharField(max_length=50)
    brand=models.CharField(max_length=50)
    arrived_date=models.DateField(blank=True,null=True)
    amount=models.IntegerField()
    in_price=models.FloatField()
    out_price=models.FloatField()
    measure=models.CharField(max_length=100,blank=True,null=True)
    branch=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True,blank=True)
    date=models.DateField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE)
    address=models.CharField(max_length=50)
    store_name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(AbstractUser):
    is_admin=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_sales=models.BooleanField(default=False)
class Record(models.Model):
    product=models.ForeignKey(Product,on_delete=CASCADE)
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    payed=models.FloatField()
    total_price=models.FloatField()
    loan=models.FloatField(default=0)
    quantity=models.IntegerField()
    date=models.DateField()