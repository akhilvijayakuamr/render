from django.shortcuts import render, redirect
from .forms import CouponForm
from django.contrib import messages
from .models import Coupon
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


# add coupon


def add_coupon(request):
    if 'admin' in request.session:
        form = CouponForm()
        if request.method == 'POST':
            form = CouponForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('view_coupon')
            else:
                messages.info(request, 'Please Enter valid information')
        context ={'form':form}
        return render(request, 'coupon/add_coupon.html', context)
    return redirect('admin')


# coupon view

def view_coupon(request):
    if 'admin' in request.session:
        val = Coupon.objects.all()
        context ={'val':val}
        return render(request, 'coupon/coupon_view.html', context)
    return redirect('admin')



# Update copon 

def update_coupon(request, cid):
        if 'admin' in request.session:
            try:
                val = Coupon.objects.get(id = cid)
            except ObjectDoesNotExist:
                    return redirect('view_coupon')
            form = CouponForm(instance = val)
            if request.method == "POST":
                    form = CouponForm(request.POST, instance=val)
            if form.is_valid():
                    form.save()
                    return redirect('view_coupon')    
            else:
                    messages.info(request, 'Please Enter valid datas')
            context = {'form' : form}     
            return render(request, 'coupon/edit_coupon.html', context)
        else:
             return redirect('admin')



# Delete coupon


def delete_coupon(request, cid):
    if 'admin' in request.session:
        val = Coupon.objects.get(id = cid)
        val.delete()
        return redirect('view_coupon')
    else:
         return redirect('admin')

