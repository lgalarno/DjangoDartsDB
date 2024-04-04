from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import CreatePlayer, PlayerDelete, PlayerUpdate, PlayerDetailView, PlayersListView

app_name = 'playersmanagement'

urlpatterns = [
    path('', PlayersListView.as_view(), name="PlayersList"),
    path('create-player/', login_required(CreatePlayer.as_view()), name="CreatePlayer"),
    path('delete-player/<int:id>/<slug>/', login_required(PlayerDelete.as_view()), name="DeletePlayer"),
    path('player/<int:id>/<slug>/change/',login_required(PlayerUpdate.as_view()), name="UpdatePlayer"),
    path('<int:id>/<slug>/', PlayerDetailView.as_view(), name="PlayerDetail"),
]

