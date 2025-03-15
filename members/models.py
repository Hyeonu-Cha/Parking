from django.db import models
from django.contrib.auth.models import User as user

class User(models.Model):

    username = models.CharField(primary_key=True, blank=False, unique=True, max_length=20)
    #admin = models.BooleanField()
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=20, blank=False, null=False)

    f_name = models.CharField(max_length=20, null=False)
    l_name = models.CharField(max_length=20, null=False)
    mobile = models.IntegerField()
    
    bankaccount = models.CharField(max_length=20, blank=True, null=True)
    birth = models.DateField()


class Property(models.Model):
    id  = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=20,default="")
    providerid = models.ForeignKey(user, on_delete=models.CASCADE)

    suburb = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    postal = models.IntegerField()

    parking_allign = models.CharField(max_length=30)
    parking_type = models.CharField(max_length=30)

    description = models.CharField(max_length=30)
    ev = models.BooleanField()
    handicap = models.BooleanField()
    price_weekday = models.FloatField(max_length=5)
    price_weekend = models.FloatField(max_length=5)

    status = models.CharField(max_length=20)
    deleted = models.BooleanField()
    property_image = models.ImageField(null=True, blank=True, upload_to="property_images/")

class RequestModel(models.Model):
    id  = models.AutoField(unique=True, primary_key=True)
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    providerid = models.ForeignKey(user,related_name="requested_providerid", on_delete=models.CASCADE)
    propertyid = models.ForeignKey(Property, on_delete=models.CASCADE)
    property_image = models.ImageField(null=True, blank=True, upload_to="property_images/")
    price = models.FloatField(max_length=20)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    booking_cost = models.FloatField(max_length=20)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class RewardPoints(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    userid = models.ForeignKey(user, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    description = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

'''
class Request(models.Model):   
    id = models.IntegerField(max_length=20) 
    userid = models.IntegerField(max_length=20)
    parkingid = models.IntegerField(max_length=20)
    providerid = models.IntegerField(max_length=20)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    totalprice = models.FloatField(max_length=20)
    status = models.BooleanField()
    
class Vechicle(models.Model):
    id = models.ForeignKey(User, on_delete=models.CASCADE)
    width = models.FloatField(max_length=20)
    length = models.FloatField(max_length=20)
    detail = models.FloatField(max_length=100)

class Provider(models.Model):
    userid = models.IntegerField(max_length=30)
    requests = models.CharField(max_length=30)'''
class Messages(models.Model):
    id  = models.AutoField(unique=True, primary_key=True)
    sender = models.ForeignKey(user, on_delete=models.CASCADE)
    receiver = models.CharField(blank=False, max_length=20)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)