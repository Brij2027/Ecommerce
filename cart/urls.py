from django.urls import path,include
from . import views
from register.views import signin

app_name = 'cart'

urlpatterns = [
    path('',views.showcart,name="show_cart"),
    path('<int:id>',views.showcart,name="show_cart"),
    path('getcartdata',views.get_cart_data,name = "get_cart_page"),
    path('updatecartdata',views.update_cart_data,name="update_cart_page"),
    path('processingpayment',views.paymenthandler,name="process_payment"),
    path('Paymentdone',views.payment_done,name="paymentdone"),
    path('register/',signin),
]
