from django.urls import path
from . import views

urlpatterns = [

    path('user_view_account/', views.user_view_account, name='user_view_account'),    #-> User view account itself
    path('add_address/', views.add_address, name='add_address'),   #-> User view account path
    path('delete_address/<str:aid>/', views.delete_address, name="delete_address"),       #-> Delete address
    path('address_view/', views.address_view, name="address_view"),      #->   Address view 
    path('orders_view/', views.orders_view, name="orders_view"),        #->   Orders view
    path('specific_item/<str:oid>/', views.specific_item, name='specific_item'),      #-> specific order
    path('cancel_order/<str:oid>/', views.cancel_order, name='cancel_order'),     #-> cancel order
   

    
]