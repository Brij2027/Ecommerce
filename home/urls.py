from django.urls import path,include
from . import views
from account import urls as account_url
from cart import urls as cart_url



urlpatterns = [
    path('',views.home,name='home'),
    path('product/<int:id>/',views.products,name = 'product_page'),
    path('save/<int:id>/',views.save_data,name='save'),
    path('categories/<str:category>/<int:page_number>',views.category_data,name='category'),
    path('search/<str:q>/<int:page_number>',views.search_data,name='search'),
    
    
]
