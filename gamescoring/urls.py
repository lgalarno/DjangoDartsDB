from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'gamescoring'

urlpatterns = [
    path('ScoreConfirm/', login_required(views.ScoreConfirm), name = "ScoreConfirm" ),
    path('SaveScore/', login_required(views.SaveScore), name = "SaveScore" ),
    path('NewScore/', login_required(views.NewScore), name = "NewScore" ),
    path('<category>/',login_required(views.EnterScore), name = "EnterScore" ),
]