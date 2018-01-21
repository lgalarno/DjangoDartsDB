from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = 'scoretable'

urlpatterns = [
    path('csv/<category>/', login_required(views.csvweb), name = "csvweb"),
    path('zip/', login_required(views.csvzip), name = "csvzip"),
    path('download/<filename>', login_required(views.downloadzip), name = "downloadzip"),
    path('upload_csv/', login_required(views.upload_csv), name = "upload_csv"),
    path('<category>/', views.webtables, name = "webtables"),
]
