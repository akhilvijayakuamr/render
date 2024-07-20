from django.urls import path
from . import views

urlpatterns = [

        path('order_manage/', views.order_manage, name='order_manage'),     #-> Admin Order manage
        path('order_delete/<str:oid>/', views.order_delete, name='order_delete'),     #-> Order Delete
        path('update_status/', views.update_status, name='update_status'),  #-> Update status 
        path('pdf_view/<str:oid>/', views.pdf_view, name="pdf_view"),  #-> pdf view
        # path('add')
       
]
