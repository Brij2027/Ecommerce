from django.db import models
from home.models import product
from django.db.models import DO_NOTHING
from django.contrib.auth.models import User

# Create your models here.
class myorder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    myproduct = models.ForeignKey(product,on_delete=DO_NOTHING)
    myrating = models.IntegerField(default=0)
    
