from django.shortcuts import render, redirect
from .models import Main_category
from . froms import CategoreyForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


# View Category

def category_view(request):
        if 'admin' in request.session:
                cat = Main_category.objects.all()
                context={'cat' : cat}
                return render(request, 'main_category_app/main_category_view.html', context )
        else:
                return redirect('admin')
        




# Add  Category

def category_add(request):
        if 'admin' in request.session:
                form = CategoreyForm()
                if request.method == "POST":
                        form = CategoreyForm(request.POST, request.FILES)
                if form.is_valid():
                        form.save()
                        return redirect('category_view')
                else:
                        messages.info(request, 'Enter valid datas')
                context = {'form' : form}
                return render(request, 'main_category_app/main_category.html', context)
        else:
                return redirect('admin')
    


# Update Category

def categorey_update(request, pid):
        if 'admin' in request.session:
                try:
                        val = Main_category.objects.get(id = pid)
                except ObjectDoesNotExist:
                        return redirect('admin_home')
                form = CategoreyForm(instance = val)
                if request.method == "POST":
                        form = CategoreyForm(request.POST, request.FILES, instance=val)
                if form.is_valid():
                        form.save()
                        return redirect('category_view')    
                else:
                        messages.info(request, 'Please Enter valid datas')
                context = {'form' : form}     
                return render(request, 'main_category_app/main_category_update.html', context)
        else:
                return redirect('admin')
    
# Delete Categorey
     

def categorey_delete(request, pid):
        if 'admin' in request.session:
                try:
                        cat = Main_category.objects.filter(id = pid)
                except ObjectDoesNotExist:
                        return redirect('category_view')
                cat.delete()
                return redirect('category_view')
        else:
                return redirect('admin')



# User category view


def user_categorey_view(request):
        if 'username' in request.session:
                try:
                        cat = Main_category.objects.filter(status = 0)
                except ObjectDoesNotExist:
                        return redirect('user_home')
                context = {'cat':cat}
                return render(request, 'main_category_app/user_category.html', context)
        else:
                return redirect('/')
       

    

# Hide Category

def hide_category(request, cid):
        if 'admin' in request.session:
                try:
                        cat = Main_category.objects.get(id = cid)
                except ObjectDoesNotExist:
                        return redirect('category_view')
                cat.status = True
                cat.save()
                return redirect('category_view')
        else:
                return redirect('admin')


# Unhide Categort


def unhide_category(request, cid):
        if 'admin' in request.session:
                try: 
                        cat = Main_category.objects.get(id = cid)
                except ObjectDoesNotExist:
                        return redirect('category_view')
                cat.status = False
                cat.save()
                return redirect('category_view')
        else:
                return redirect('admin')


# Search categories


def search_categories(request):
        if 'admin' in  request.session:
                if request.method == 'POST':
                        quarey = request.POST.get('q')
                        val = Main_category.objects.filter(name__icontains=quarey)
                context={'cat' : val}
                return render(request, 'games/games_view.html', context )
        else:
                return redirect('admin')