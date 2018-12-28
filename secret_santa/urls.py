"""secret_santa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from hohoho.views import (signup, MainView, NewGameView, GameView, JoinGameView, DeleteGameView,
                          GenerateView, StartGameView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), {'next_page': '/'}, name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': '/'}, name='logout'),
    path('signup/', signup, name='signup'),

    path('', MainView.as_view(), name='main'),
    path('new_game', NewGameView.as_view(), name='new-game'),
    path('game/<int:game_pk>', GameView.as_view(), name='game'),
    path('delete_game/<int:user_game_pk>', DeleteGameView.as_view(), name='delete_game'),
    path('join_game/<int:game_pk>', JoinGameView.as_view(), name='join-game'),
    path('generate_game/<int:game_pk>', GenerateView.as_view(), name='generate-game'),
    path('start_game/<int:game_pk>', StartGameView.as_view(), name='start-game'),

]
