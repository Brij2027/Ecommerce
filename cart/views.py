from django.shortcuts import redirect, render
from home.models import product
from .models import cartproduct
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.sites import requests
from register.models import profile
from home.views import categories
from account.models import myorder 


# Create your views here.
def showcart(requests,id=0):
    if not requests.user.is_authenticated:
        return redirect('register/')
    else:
        if id !=0:
            productobj = product.objects.get(id=id)
            if (cartproduct.objects.filter(productobj=id).count() == 0 ):
                cartobj = cartproduct.objects.create(productobj = productobj)
                cartobj.save()
            else:
                cartobj = cartproduct.objects.get(productobj=id)
                cartobj.quantity = cartobj.quantity+1
                cartobj.save()

        profileobj = profile.objects.get(user=requests.user)
        context = {
            "title":"-Cart",
            "address":profileobj.my_address,
            "loggedin" : requests.user.is_authenticated,
            "categories":categories,
        }

        return render(requests,template_name='cart.html',context=context)

def get_cart_data(requests):
    if requests.method == "GET":
        cartobj = list(cartproduct.objects.values())
        jsondata = []
        i = 0
        for cart in cartobj:
            productobj =product.objects.get(id = cart['productobj_id'])
            jsondata.append({"name":productobj.name,"price":productobj.price*cart['quantity'],"serial":cart['serial'],"quantity":cart['quantity'],"productid":cart['productobj_id']})
            i+=1
        
        return JsonResponse(jsondata,safe=False)

def update_cart_data(requests):
    if requests.method == "POST":
        plus = requests.POST.get('plus')
        minus = requests.POST.get('minus')
        remove = requests.POST.get('remove')

        if plus:
            productid = requests.POST.get('productid')
            productobj = product.objects.get(id = productid)
            cartobj = cartproduct.objects.get(productobj_id=productid)
            cartobj.quantity = cartobj.quantity+1
            cartobj.save()
            return JsonResponse({"data":cartobj.quantity,"price":productobj.price*cartobj.quantity})
        elif minus:
            productid = requests.POST.get('productid')
            productobj = product.objects.get(id = productid)
            cartobj = cartproduct.objects.get(productobj_id=productid)
            cartobj.quantity = cartobj.quantity-1
            cartobj.save()
            if (cartobj.quantity == 0):
                cartobj.delete()
                return JsonResponse({"data":0,"len":cartproduct.objects.all().count()})               
            return JsonResponse({"data":cartobj.quantity,"price":productobj.price*cartobj.quantity})
        else:
            productid = requests.POST.get('productid')
            cartobj = cartproduct.objects.get(productobj_id=productid)
            cartobj.delete()
            return JsonResponse({"data":cartproduct.objects.all().count()})

def paymenthandler(requests):
    if requests.method == "POST":
        productarr = requests.POST.get('productarr')
        totalprice = requests.POST.get('price')
        address = requests.POST.get('address')
        address = list(filter(bool,address.splitlines()))  

        #go to payment page
        return render(requests,'paypal.html',{"price": totalprice,"prodlist":productarr})

def payment_done(requests):
    if requests.method == "POST":
        productlist = requests.POST.get("prodlist")
        productlist = productlist.split(',')
        for prod in productlist:
            id,quantity = prod.split(";")
            cartobj = cartproduct.objects.get(productobj_id=id)
            cartobj.delete()
            myorder.objects.create(user=requests.user,myproduct = product.objects.get(id=id))
        
        profileobj = profile.objects.get(user=requests.user)
        context = {
            "address":profileobj.my_address,
            "loggedin" : requests.user.is_authenticated,
            "categories":categories,
            "purchasedone":True,
        }
        return render(requests,template_name='cart.html',context=context)


    


