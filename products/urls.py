from django.urls import path
from . import views


urlpatterns = [

    path('products_add/', views.products_add, name="products_add"),  # -> Add Products path
    path('products_view/', views.products_view, name="products_view"),  #-> View Products path
    path('products_update/<str:pid>/', views.products_update, name='products_update'),  #-> Update Products path
    path('products_delete/<str:pid>/', views.products_delete, name="products_delete"), #-> Delete Products path
    path('image_add/', views.image_add, name='image_add'),  #-> Add Image
    path('image_view/<str:pid>/', views.image_view, name='image_view'), #-> View Image path
    path('image_delete/<str:pid>/', views.image_delete, name='image_delete'), #-> Image Delete path
    path('user_products_view/<str:pid>/', views.user_products_view, name="user_products_view"), #-> User Products View path
    path('user_product_view/<str:mid>/<str:gid>/<str:pid>/', views.user_product_view, name="user_product_view"),  #-> User Productn View path
    path('search_products/', views.search_products, name = "search_products"),      #-> search products
    path('add_review/', views.add_review, name='add_review'),   #-> add review
    path('product_price/<int:pid>/<int:low_price>/<int:high_price>/', views.products_price, name="product_price"),     #-> product price
    path('max_to_min/<int:pid>/', views.max_to_min, name='max_to_min'),      #-> max_to_min path
    path('min_to_max/<int:pid>/', views.min_to_max, name="min_to_max"),     #-> min_to_max path      

]