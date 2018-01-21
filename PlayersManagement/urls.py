from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'PlayersManagement'

urlpatterns = [
    path('', views.PlayersListView.as_view(), name = "PlayersList"),
    path('create-player/', login_required(views.CreatePlayer.as_view()), name = "CreatePlayer"),
    path('delete-player/<name>/', login_required(views.PlayerDelete.as_view()), name = "DeletePlayer"),
    path('player/<name>/change/',login_required(views.PlayerUpdate.as_view()), name = "UpdatePlayer"),
    path('<name>/', views.PlayerDetailView.as_view(), name = "PlayerDetail"),
]

