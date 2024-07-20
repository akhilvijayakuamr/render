from django.urls import path
from . import views


urlpatterns = [

    path('user_view/', views.view_users, name = 'user_view'),       #-> User view path
    path('specific_user/<str:uid>/', views.view_user, name = 'specific_user'),        #-> Specific user view
    path('delete_user/<str:uid>/', views.delete_user, name = 'delete_user'),     #-> Delete user
    path('customer/<int:customer_id>/block/', views.block_customer, name='block_customer'),   #-> Block user
    path('customer/<int:customer_id>/unblock/', views.unblock_customer, name='unblock_customer'),   #-> Unblock user
]