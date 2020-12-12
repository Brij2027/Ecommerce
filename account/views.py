from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from register.models import profile
from .models import myorder
from django.http import JsonResponse
from home.models import product, rating
from math import ceil
from home.views import categories


# Create your views here.

def show_account(requests,*args,**kwargs):
    if not requests.user.is_authenticated:
        return redirect('register/')
    else:
        profileobj = profile.objects.get(user=requests.user)
        myorderobj = myorder.objects.filter(user=requests.user)
        context = {
            "title":"-Account",
            "profileobj":profileobj,
            "myorderobj":myorderobj,
            "loggedin" : requests.user.is_authenticated,
            "categories":categories,
        }
        return render(requests,template_name='account.html',context=context)

def order(requests,name):
    myorderobj = myorder.objects.get(user=requests.user)
    context = {
        "myorderobj":myorderobj,
    }
    return render(requests,template_name='order.html',context=context)

def change_data(requests):
    if requests.method == "POST":
        val = requests.POST['change_val']
        col = requests.POST.get('col_name')
        if (col == "username"):
            user = requests.user
            user.username = val
            user.save()
            profileobj = profile.objects.get(user=user)
            profileobj.save()
        else:
            if (col == 'gender'):
                profileobj = profile.objects.filter(user=requests.user).update(gender= val)
            elif(col == 'my_address'):
                profileobj = profile.objects.filter(user=requests.user).update(my_address=val)
            elif(col == 'phone'):
                profileobj = profile.objects.filter(user=requests.user).update(phone=val)
        return HttpResponse(val+col)

def get_data(requests):
    if requests.method == "GET":
        profileobj = profile.objects.get(user=requests.user)
        return JsonResponse({"username":profileobj.user.username,"gender":profileobj.gender,"phone":profileobj.phone,
        "address":profileobj.my_address,"image":profileobj.image})

def setrating(requests):
    if requests.method == "POST":
        index = int(requests.POST.get("index"))
        productname,productid = requests.POST.get("productid").split(":")
        length = int(requests.POST.get("length"))

        print(index)
        if (index > length):
            index = ceil(index//length)

        productobj = product.objects.get(id=productid)
        myorderobjlist = myorder.objects.filter(myproduct=productobj)
        for myorderobj in myorderobjlist:
            myorderobj.myrating = index
            myorderobj.save()
        if (rating.objects.filter(product=productobj).count() == 0):
            rating.objects.create(product=productobj,rating = index,ratingusers=1)
        else:
            ratingobj = rating.objects.get(product=productobj)
            ratingobj.ratingusers+=1
            if (ratingobj.rating > (index)):
                ratingobj.rating -= (index)//ratingobj.ratingusers
            else:
                ratingobj.rating += (index)//ratingobj.ratingusers
            ratingobj.save()
            print(ratingobj.rating,ratingobj.ratingusers)

        return HttpResponse(index)


