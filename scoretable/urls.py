from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from scoretable import views

app_name = 'scoretable'

urlpatterns = [
    path('csv/<category>/', login_required(views.csvweb), name="csvweb"),
    path('zip/', login_required(views.csvzip), name="csvzip"),
    path('download/<slug>/', login_required(views.downloadzip), name="downloadzip"),
    path('deletez/<int:id>/', login_required(views.deletezip), name="deletezip"),
    path('deleteg/<int:id>/', login_required(views.deletegame), name="deletegame"),
    path('editg/<int:id>/', login_required(views.editgame), name="editgame"),
    path('upload_csv/', staff_member_required(views.upload_csv), name="upload_csv"),
    path('<category>/', views.webtables, name="webtables"),
]
