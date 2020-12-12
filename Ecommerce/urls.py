"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from register import urls as register_url
from home import urls as home_url
from account import urls as account_url
from cart import urls as cart_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',include(register_url)),
    path('',include(home_url)),
    path('home/',include(home_url)),
    path('account/',include(account_url)),
    path('cart/',include(cart_url)),
]
