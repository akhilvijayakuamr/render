from django.shortcuts import render, redirect
from .forms import BannerForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Banner
# Create your views here.

#add banner

def add_banner(request):
    if 'admin' in request.session:
        form = BannerForm()
        if request.method == "POST":
                form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
                form.save()
                return redirect('view_banner')
        else:
            messages.info(request, 'Please enter valid datas')
        context = {'form' : form}
        return render(request, 'banner/banner_add.html', context)
    else:
         return redirect('admin')


# update banner


def update_banner(request, bid):
    if 'admin' in request.session:
        try:
            val = Banner.objects.get(id = bid)
        except ObjectDoesNotExist:
            return redirect('admin_home')
        form = BannerForm(instance = val)
        if request.method == "POST":
            form = BannerForm(request.POST, request.FILES, instance=val)
        if form.is_valid():
            form.save()
            return redirect('view_banner')  
        else:
            messages.error(request, 'Please enter valid datas')  
        context = {'form' : form}     
        return render(request, 'banner/banner_update.html', context)
    return redirect('admin')


#def banner view

def view_banner(request):
    if 'admin' in request.session:
        try:
            cat = Banner.objects.all()
        except ObjectDoesNotExist:
            return redirect('admin_home')
        context={'cat' : cat}
        return render(request, 'banner/banner_view.html', context)
    else:
         return redirect('admin')
         

# delete banner

def delete_banner(request, bid):
        if 'admin' in request.session:
            try:
                ba = Banner.objects.filter(id = bid)
            except ObjectDoesNotExist:
                    return redirect('admin_home')
            ba.delete()
            return redirect('view_banner')
        else:
             return redirect('admin')