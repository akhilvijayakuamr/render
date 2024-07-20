from django.urls import path
from .import views


urlpatterns = [

        path('category/', views.category_add, name='category'),             #-> Add Category path
        path('category_view/', views.category_view, name='category_view'),  #-> View Category path
        path('categorey_update/<str:pid>/', views.categorey_update, name='categorey_update'),   #-> Category Update path
        path('category_delete/<str:pid>/', views.categorey_delete, name='category_delete'),     #-> Categoery Delete path
        path('user_category_view/', views.user_categorey_view, name='user_category_view'),      #-> User Category View path
        path('hide_category/<str:cid>/', views.hide_category, name='hide_category'),   #-> Hide Category
        path('unhide_category/<str:cid>/', views.unhide_category, name='unhide_category'),  #-> Unhide Category
        path('search_categories/',views.search_categories, name='search_categories'),          #-> search categories
]