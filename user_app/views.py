from django.shortcuts import render, redirect
from auth_app . models import Customuser
from .forms import Userupdateform
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


# View users 


def view_users(request):
    if 'admin' in request.session:
        us = Customuser.objects.filter(is_superuser = False)
        context = {'us' : us}
        return render(request, 'user_app/user_view.html', context)
    else:
        return redirect('admin')
    


# View all details in specific user
    

def view_user(request, uid):
        if 'admin' in request.session:
            us = Customuser.objects.filter(id = uid)
            context = {'us' : us}
            return render(request, 'user_app/specific_user.html', context)
        else:
             return redirect('admin')
    



#  Delete user
    
def delete_user(request, uid):
        if 'admin' in request.session:
            u = Customuser.objects.filter(id = uid)
            u.delete()
            return redirect('user_view')
        else:
             return redirect('admin')
    



# UnBlock user 
    

def unblock_customer(request,customer_id):
        if 'admin' in request.session:
            try:
                customer = Customuser.objects.get(id=customer_id)
            except ObjectDoesNotExist:
                return redirect('user_view')  
        
            customer.is_active = True
            customer.save()

            return redirect('user_view')
        else:
             return redirect('admin')


# Block user

def block_customer(request,customer_id):
        if 'admin' in request.session:
            try:
                customer = Customuser.objects.get(id=customer_id)
            except Customuser.DoesNotExist:
                return redirect('user_view')  
            customer.is_active = False
            customer.save()
            return redirect('user_view')
        else:
             return redirect('admin')
                


    

