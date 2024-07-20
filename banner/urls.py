from django.urls import path
from . import views

urlpatterns=[
    path('add_banner/', views.add_banner, name='add_banner'),       #-> add banner
    path('update_banner/<str:bid>/', views.update_banner, name='update_banner'),      #-> update banner
    path('view_banner/', views.view_banner, name="view_banner"),    #-> view banner
    path('delete_banner/<str:bid>/', views.delete_banner, name='delete_banner'),      #-> banner delete
]