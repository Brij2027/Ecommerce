from django.db import models
import csv
from django.db.models import DO_NOTHING

'''def generate_db():
    with open('database1.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = product.objects.get_or_create(
                    id = row[0],
                    name=row[1],
                    price=row[2],
                    image=row[3],
                    offer=row[4],
                    availability = row[5],
                    categories = row[6]
                    )
'''

# Create your models here.
class product(models.Model):
    name = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=9)
    image = models.TextField()
    offer = models.TextField(max_length=5)
    availability = models.TextField(max_length=3)
    categories = models.TextField()


class comment(models.Model):
    product_id = models.IntegerField(); 
    user = models.TextField()
    review = models.TextField()
    image = models.TextField(default="")
    date = models.DateField(auto_now=True)

class rating(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    ratingusers = models.IntegerField(default=0)
