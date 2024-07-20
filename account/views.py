from django.shortcuts import render, redirect
from user_app . models import Address
from django.contrib import messages
import re
from cart.models import Cart
from checkout.models import Order, OrderItem
from auth_app .models import Customuser
from wallet.models import Wallet

# Create your views here.

# View account page


def user_view_account(request):
    if 'username' in request.session:
        user = request.user
        us = Customuser.objects.filter(id = user.id)
        context = {'us':us}
        return render(request, 'account/user_dashboard.html', context)
    else:
        return redirect('/')

# Address view


def address_view(request):
    if 'username' in request.session:
        us = Address.objects.filter(user = request.user, is_delete = False)
        context = {'us' : us}
        return render(request, 'account/address_view.html', context)
    else:
        return redirect('/')


# Add user address

def add_address(request):
    if 'username' in request.session:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            house_no = request.POST.get('house_no')
            post_code = request.POST.get('post_code')
            state = request.POST.get('state')
            street = request.POST.get('street')
            phone_no = request.POST.get('phone_number')
            city = request.POST.get('city')

            if (not full_name or
                not house_no or
                not post_code or
                not state or
                not street or
                not phone_no or
                not city ):
                messages.info(request, 'Please fill all fields')
            elif post_code and not re.match(r'^\d{6}$', post_code):
                messages.info(request, 'Please fill valid 6 digit pincode')
            elif  not re.match(r'^[789]\d{9}$', phone_no):
                messages.info(request, 'Please fill valid phone number')
            else:
                user = request.user
                address = Address(user = user,
                             full_name = full_name,
                             house_no = house_no,
                             state = state,
                             street = street,
                             post_code = post_code,
                             phone_no = phone_no,
                             city = city)
                address.save()
                return redirect('user_home')
        return render(request, 'account/add_address.html')
    return redirect('/')


# Delete user address

def delete_address(request, aid):
    if 'username' in request.session:
        add = Address.objects.filter(id = aid)
        add.delete()
        return redirect('user_view_account')
    else:
        return redirect('/')

# Orders View

def orders_view(request):
    if 'username' in request.session:
        item = OrderItem.objects.filter(order__user = request.user).order_by('-id')
        context = {'item':item}
        return render(request, 'account/orders.html', context)
    else:
        return redirect('/')
#Order specific view

def specific_item(request, oid):
    if 'username' in request.session:
        item = OrderItem.objects.get(id = oid)
        context = {'item' : item}
        return render(request, 'account/orders_view.html', context)
    else:
        return redirect('/')



#Cancel Order

def cancel_order(request, oid):
    if 'username' in request.session:
        val = Order.objects.get(id = oid)
        if val.status == "refunded":
            messages.info(request, 'Allready amount is refunded')
            return redirect('orders_view')
        if val.status == "Completed":
            messages.info(request, 'Allready order is completed')
            return redirect('orders_view')
        if val.status == "Cancelled":
            messages.info(request, 'Allready order is cancelled ')
            return redirect('orders_view')
        if val.payment_type == 'razorpay':
            Wallet.objects.create(user = request.user,
                                order = val,
                                amount = val.amount,
                                status = 'Cancel order')
            val.status = "refunded"
            val.save()
            return redirect('orders_view')
        else:
            val.status = "Cancelled"
            val.save()
            return redirect('orders_view')
    else:
        return redirect('/')
        
    

