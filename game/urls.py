from django.urls import path
from . import views

urlpatterns = [
    path('initialize_game/', views.InitializeGameView,
         name="game_create"),
    path('games/', views.GameListView.as_view(),
         name="game_list"),
    path('history/', views.HistoryGameListView.as_view(),
         name="history_list"),
    path('game/<int:pk>/', views.GameView,
         name="game"),
    path('game/<int:pk>/delete', views.GameDeleteView.as_view(),
         name='confirm_delete'),
]