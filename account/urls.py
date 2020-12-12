from django.urls import path
from . import views
from register.views import signin
from home.views import products

app_name = 'account'

urlpatterns = [
    path('',views.show_account,name='account_page'), 
    path('order/<int:id>',products,name='order_page'),
    path('change/',views.change_data,name='change_page'),
    path('get/',views.get_data,name='get_page'),
    path('setrating/',views.setrating,name='set_rating'),
    path('register/',signin),
]