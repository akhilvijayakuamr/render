from django.urls import path
from . import views

urlpatterns = [

    path('check_out/', views.check_out, name='check_out'),  #-> Checkout path
    path('check_address/', views.check_address, name='check_address' ),      #-> view address
    path('place_order/', views.place_order, name="place_order"),        #-> place order
    path('coupon/', views.coupon, name="coupon"),   #-> coupon
    path('razorpay/<int:address_id>/', views.razorpay, name='razorpay'),  #-> razorpay 
    path('proceedtopay/', views.proceedtopay, name='proceedtopay'),  #-> proceedtopay
    path('wallet_order/', views.wallet_order, name='wallet_order'), #-> wallet use order
    
   
   
]