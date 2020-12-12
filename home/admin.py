from django.contrib import admin
from .models import product,comment
from home.models import rating

# Register your models here.
admin.site.register(product)
admin.site.register(comment)
admin.site.register(rating)