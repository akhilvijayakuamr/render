from django.urls import path
from . import views

urlpatterns = [

    path('admin_home/', views.admin_home, name = 'admin_home'),       #-> Admin home path
    path('admin/', views.admin_login, name = 'admin'),        #-> Admin login path
    path('admin_logout/', views.admin_logout, name='admin_logout'),      #-> Admin logout path
   

]