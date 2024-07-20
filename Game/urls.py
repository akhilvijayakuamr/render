"""
URL configuration for Game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('auth_app.urls')),     #-> Connect auth_app urls
    path('', include('main_category_app.urls')),   #-> Connect main_category_app urls
    path('', include('games.urls')),      #->  Connect games urls
    path('', include('products.urls')),     #-> Connect products urls
    path('', include('admin_auth_app.urls')), #-> Connect admin_auth_app urls
    path('', include('user_app.urls')),   #-> Connect user_app urls
    path('', include('account.urls')),      #-> Connect account urls
    path('', include('cart.urls')),     #-> Connect cart urls
    path('', include('wishlist.urls')),     #-> Connect Wishlist app urls
    path('', include('checkout.urls')),     #-> Connect checkout app urls
    path('', include('order.urls')),       #-> Connect Order app urls
    path('', include('coupon.urls')),       #-> Connect coupon app urls
    path('', include('report_app.urls')),    #-> Connect report app urls
    path('', include('wallet.urls')),       #-> Connect wallet app urls
    path('', include('banner.urls')),       #-> Connect banner app urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
