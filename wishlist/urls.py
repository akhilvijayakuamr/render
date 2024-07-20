from django.urls import path
from . import views

urlpatterns = [

    path('wishlist/', views.wish_list, name='wishlist'),        #-> View wishlist path
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),        #-> Add to wishlist
    path('remove_wishlsit/<str:wid>/', views.remove_wishlist, name='remove_wishlist'),        #-> Remove to wishlist
]