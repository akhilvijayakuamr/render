from django.urls import path
from . import views


urlpatterns = [

        path('add_coupon/', views.add_coupon, name="add_coupon"),   #-> add Coupon path
        path('view_coupon/', views.view_coupon, name="view_coupon"),  #->  view Coupon
        path('update_coupon/<str:cid>/', views.update_coupon, name="update_coupon"),  #-> update Coupon
        path('delete_coupon/<str:cid>/', views.delete_coupon, name="delete_coupon"),  #-> Delete Coupon
]