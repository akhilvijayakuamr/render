from django.shortcuts import render, redirect
from django.contrib import messages
from auth_app . models import Customuser
from django.contrib.auth import login, logout
from django.views.decorators.cache import cache_control,never_cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from main_category_app.models import Main_category
from games.models import Games
from products.models import Product
from checkout.models import Order, OrderItem
from django.db.models import Sum,F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
# Create your views here.


# Admin Home


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache      
def admin_home(request):
        if 'admin' in request.session:
            total_users = Customuser.objects.count()
            total_categories = Main_category.objects.count()
            category_count = Main_category.objects.count()
            subcategory_count = Games.objects.count()
            product_count = Product.objects.count()
            total_orders = Order.objects.count()
            total_amount = Order.objects.aggregate(Sum('amount'))['amount__sum'] or 0

            context = {
                'total_orders': total_orders,
                'total_amount': total_amount,
                'total_users': total_users,
                'category_count': category_count,
                'subcategory_count': subcategory_count,
                'product_count': product_count,
                'total_categories':total_categories
            }
            return render(request, 'admin_auth_app/admin_index.html',context)
        else:
             return redirect('admin')
        




# Admin Login
    


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def admin_login(request):
        if 'admin' in request.session:
             return redirect('admin_home')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.method == 'POST':
            if not (username and password):
                 messages.info(request, 'username and password is not required')
            else:
                user = Customuser.objects.filter(username=username, is_staff = True, is_superuser = True).first()
                if user is None:
                    messages.info(request, "Incorrect User")
                else:
                    if not user.check_password(password):
                        messages.info(request, 'Incorrect Password')
                    else:
                        if user.is_active:
                            login(request,user)
                            request.session['admin'] = username
                            return redirect('admin_home')
                        else:
                            messages.info(request, "Inactive user")
        return render(request, 'admin_auth_app/admin_account_login.html')




# Admin logout



@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache  
def admin_logout(request):
     if 'admin' in request.session:
          request.session.flush()
          return redirect('admin')
     






     
