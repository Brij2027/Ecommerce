from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import DO_NOTHING
# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User,primary_key = True,on_delete=models.CASCADE)
    gender = models.CharField(blank =True,max_length=8)
    phone = models.IntegerField(blank=True,default=0)
    my_address = models.CharField(max_length=100,blank=True)
    totp = models.CharField(max_length = 5 , blank=True)
    image = models.TextField(blank=True)


    def get_otp(self):
        return self.totp
