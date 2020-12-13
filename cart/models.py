from django.db import models
from django.db.models import DO_NOTHING
from home.models import product

# Create your models here.
class cartproduct(models.Model):
    serial = models.AutoField(primary_key=True)
    productobj = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def remove(self,product):
        self.cartproduct.objects.filter(productobj=product).delete()

    def count(self):
        return self.cartproduct.objects.all()
