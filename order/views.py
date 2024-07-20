from django.shortcuts import render, redirect
from checkout.models import OrderItem, Order
from django.core.paginator import Paginator

from django.contrib import messages


# Create your views here.

# Order view admin

def order_manage(request):
    if 'admin' in request.session:
        orders = Order.objects.all().order_by('-id')
        context = {
                'orders': orders,
            }
        return render(request, 'order/admin_order.html', context)
    else:
        return redirect('admin')

# Order delete

def order_delete(request, oid):
    if 'admin' in request.session:
        val = Order.objects.filter(id = oid)
        val.delete()
        return redirect('order_manage')
    else:
        return redirect('admin')


# update status


def update_status(request):
    if 'admin' in request.session:
        if request.method == 'POST':
            status = request.POST.get('status')
            id = request.POST.get('order_id')
            order=Order.objects.get(id = id)
            order.status=status
            order.save()
            return redirect('order_manage')
    else:
        return redirect('admin')
    


# View pdf
    

def pdf_view(request, oid):
    if 'username' in request.session:
        item = OrderItem.objects.get(id = oid)
        context = {'item' : item}
        return render(request, 'order/pdf.html', context)
    else:
        return redirect('/')




        






