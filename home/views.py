from django.shortcuts import render,redirect,HttpResponse
from .models import product,comment
from django.http import JsonResponse, request
from django.contrib.sites import requests
from django.core.paginator import Paginator
import datetime
import pickle
from account.models import myorder
from home.models import rating

#global vars
#base categories only for printing
#base_categories = ['Computer','Computer Accesories','Speakers','headphones','Telivision','Other Electronics']

categories = ['Audio','Computers','Stereos','Electronics','Portable','Surround','Internal'
                    ,'Accesories','Bluetooth','Parts']
# Create your views here.

def home(requests):
    query = []

    for i in range(5):
        temp_query = product.objects.filter(categories__regex = '^'+categories[i] )[0:5]
        query.append(temp_query)
    context = {
        "title":"-Home",
        "loggedin" : requests.user.is_authenticated,
        "database" : query,
        "categories":categories,
        "recommendations": recommendations()
    }
    return render(requests,template_name='home.html',context=context)

def products(requests,id):
    productobj = product.objects.get(id=id)
    commentobj = comment.objects.filter(product_id=id)
    if (rating.objects.filter(product=productobj).count()==0):
        ratingobj = 0
    else:
        ratingobj = rating.objects.get(product=productobj)
    haspurchased = myorder.objects.filter(myproduct=productobj)
    context = {
        "productobj":productobj,
        "loggedin" : requests.user.is_authenticated,
        "categories":categories,
        "commentobj":commentobj,
        "haspurchased":haspurchased,
        "rating":ratingobj,
    }
    return render(requests,template_name='product.html',context=context)

def save_data(requests,id):
    if (requests.method == "POST"):
        print("posted")
        review = requests.POST['commentis']
        image = requests.POST['media']
        print(review,image)
        cm = comment.objects.create(product_id = id,user = requests.user.username,image = image,review = review)
        cm.save()

        return JsonResponse({"user":requests.user.username,"review":review,"date":datetime.date.today()},safe=False)

    if (requests.method == "GET"):
        commentobj = list(comment.objects.values())
        commentobj = [commdict for commdict in commentobj if commdict["product_id"] == id]
        return JsonResponse(commentobj,safe=False)
    
    return HttpResponse("hello")


def category_data(requests,category,page_number):
    temp_query = product.objects.filter(categories__regex = '^'+category )
    paginator = Paginator(temp_query,12)
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj":page_obj,
        "category":category,
        "loggedin" : requests.user.is_authenticated,
        "categories":categories,
    }
    return render(requests,template_name='categories.html',context=context)

def search_data(requests,q,page_number):
    if requests.method == "POST":
        temp_query = product.objects.filter(name__regex = '^'+q )
        if temp_query.count() == 0:
            page_obj=0
        else:
            paginator = Paginator(temp_query,12)
            page_obj = paginator.get_page(page_number)
        context = {
            "page_obj":page_obj,
            "val":q,
            "loggedin" : requests.user.is_authenticated,
            "categories":categories,
        }
        return render(requests,template_name='search.html',context=context)


def recommendations():
    file = open("./recommendationslist",'rb')
    recomm = pickle.load(file)
    allorders = myorder.objects.values()
    recommendation = []
    for order in allorders:
        temp = recomm[order['myproduct_id']]
        temp = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1],reverse=True)}
        temp = list(temp.keys())
        recommendation.extend(temp[0:5])

    recommendation = set(recommendation)

    product_recomendations = []
    for i in recommendation:
        product_recomendations.append(product.objects.get(id=i))

    return product_recomendations


    



