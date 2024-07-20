from django.urls import path
from . import views

urlpatterns = [

    path('games_add/', views.games_add, name="games_add"),  #-> Add Games path
    path('games_view/', views.games_view, name="games_view"),  #-> View Games path
    path('games_update/<str:pid>/', views.games_update, name="games_update"),  #-> Games update path
    path('games_delete/<str:pid>/', views.games_delete, name="games_delete"),   #-> Games delete path
    path('user_games_view/<str:pid>/', views.user_view_games, name="user_games_view"),   #-> User view games path
    path('hide_game/<str:gid>/', views.hide_game, name='hide_game'),   #-> Hide game path
    path('unhide_game/<str:gid>/', views.unhide_game, name='unhide_game'),    #-> Unhide game path
    path('search_game/', views.search_game, name="search_game")     #->  search games
]