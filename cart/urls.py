from django.urls import path
from . import views


urlpatterns = [


    path('cart/', views.view_cart, name='cart'),    #-> User view cart
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),   #-> Add cart path
    path('remove_cart/<str:cid>/', views.remove_cart, name='remove_cart'),    #-> Remove cart
    path('update_cart/', views.update_cart, name='update_cart' ),       #-> Update cart
    path('add_to_cart_wishlist/', views.add_to_cart_wishlist, name="add_to_cart_wishlist") #Add to cart in wishlist
]