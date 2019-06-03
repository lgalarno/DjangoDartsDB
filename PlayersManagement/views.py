from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Player

class PlayersListView(ListView):
    template_name = 'PlayersManagement/list.html'

    def get_queryset(self):
        return Player.objects.all()

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'PlayersManagement/detail.html'
    def get_object(self):
        object = get_object_or_404(Player, id=self.kwargs['id'])
        return object

class CreatePlayer(CreateView):
    context_object_name = 'Create'
    model = Player
    fields = ['name', 'description', 'picture', 'active']

class PlayerUpdate(UpdateView):
    context_object_name = 'Update'
    model = Player
    fields = ['name', 'description', 'picture', 'active']
    def get_object(self):
        object = get_object_or_404(Player, id=self.kwargs['id'])
        return object
    def get_context_data(self, **kwargs):
        context = super(PlayerUpdate, self).get_context_data(**kwargs)
        context['update_view'] = True
        return context

class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('PlayersManagement:PlayersList')
    def get_object(self):
        object = get_object_or_404(Player, id=self.kwargs['id'])
        return object

from django.http import JsonResponse

def license_check(request, username=None):
    """
    List all code snippets, or create a new snippet.
    """
    print(request)
    print( username)
    if request.method == 'GET':

        response = JsonResponse({'requestKey': 'E173663A785B72C4D75E',
                                 'activationCode': 'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
                                 'expirationDate': '05/31/2020'
                                 }, safe=False)

        return response

    elif request.method == 'POST':
        pass