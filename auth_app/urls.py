from django.urls import path
from . import views


urlpatterns=[

    path('', views.user_login, name = 'user_login'),      #-> User login path
    path('user_home/', views.user_home, name = 'user_home'),       #-> User home path
    path('user_register/', views.user_register, name = 'user_register'),        #-> User register path
    path('verify/',views.verify_signup,name='verify'),       #-> Verify OTP path
    path('user_logout/', views.user_logout, name='user_logout'),     #-> User logout
    path('for_password/', views.for_password, name='for_password'),     #-> forgot password
    path('reset_check/', views.for_verify_signup, name='reset_check'),        #-> forgot verify password
    path('reset_password/', views.reset_password, name='reset_password'),   #-> reset password
    path('password_change/', views.password_change, name='password_change'),    #-> passwordchange view
    path("password_success/",views.password_success,name="password_success"),  #-> Success urls
    path('login_back/', views.return_login, name='login_back'),     #-> login back url
    path('generate_referal/', views.generate_referral_code, name="generate_referal"),   #-> generate referal
    path('search_products/', views.searchproduct, name="search_products"),   #-> search products
    path("productlist/",views.productlist_ajax,name="productlist"),     #-> product list
    

]