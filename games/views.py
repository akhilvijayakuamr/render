from django.shortcuts import render, redirect
from .models import Games
from .forms import GameForm
from main_category_app.models import Main_category
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
# Create your views 


         
                    
def games_view(request):
        if 'admin' in request.session:
                try:
                        cat = Games.objects.all()
                except ObjectDoesNotExist:
                        return redirect('admin_home')
                context={'cat' : cat}
                return render(request, 'games/games_view.html', context )
        else:
                return redirect('admin')




# Add  Category

def games_add(request):
        if 'admin' in request.session:
                form = GameForm()
                if request.method == "POST":
                        form = GameForm(request.POST, request.FILES)
                if form.is_valid():
                        form.save()
                        return redirect('games_view')
                else:
                        messages.info(request, 'Please enter valid datas')
                context = {'form' : form}
                return render(request, 'games/games_add.html', context)
        else:
                return redirect('admin')
    


# Update Games

def games_update(request, pid):
        if 'admin' in request.session:

                try:
                        val = Games.objects.get(id = pid)
                except ObjectDoesNotExist:
                        return redirect('admin_home')
                form = GameForm(instance = val)
                if request.method == "POST":
                        form = GameForm(request.POST, request.FILES, instance=val)
                if form.is_valid():
                        form.save()
                        return redirect('games_view')  
                else:
                        messages.error(request, 'Please enter valid datas')  
                context = {'form' : form}     
                return render(request, 'games/games_update.html', context)
        else:
                return redirect('admin')
        
     
    
# Games Delete
     

def games_delete(request, pid):
        if 'admin' in request.session:
                try:
                        cat = Games.objects.filter(id = pid)
                except ObjectDoesNotExist:
                        return redirect('admin_home')
                cat.delete()
                return redirect('games_view')
        return redirect('admin')



# User View Game


def user_view_games(request, pid):
        if 'username' in request.session:
                if(Main_category.objects.filter(status = 0, id = pid)):
                        gam = Games.objects.filter(main_category__id = pid, status = 0)
                        context = {'gam':gam}
                        return render(request, 'games/user_games.html', context)
                else:
                        messages.error(request, 'Games are available')
                        return redirect('user_category_view')
        else:
                return redirect('/')


# Hide Game
        
def hide_game(request, gid):
        if 'admin' in request.session:
                try:
                        gam = Games.objects.get(id = gid)
                except ObjectDoesNotExist:
                        return redirect('games_view')
        
                gam.status=True
                gam.save()
                return redirect('games_view')
        else:
                return redirect('admin')




# Unhide Games



def unhide_game(request, gid):
        if 'admin' in request.session:
                try:
                        gam = Games.objects.get(id = gid)
                except ObjectDoesNotExist:
                        return redirect('games_view')
        
                gam.status = False
                gam.save()
                return redirect('games_view')
        else:
                return redirect('admin')


# Search game


def search_game(request):
        if 'admin' in request.session:
                if request.method == 'POST':
                        quarey = request.POST.get('q')
                        val = Games.objects.filter(name__icontains=quarey)
                context={'cat' : val}
                return render(request, 'games/games_view.html', context )
        else:
                return redirect('admin')




