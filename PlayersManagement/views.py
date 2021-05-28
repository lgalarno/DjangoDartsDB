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
        obj = get_object_or_404(Player, id=self.kwargs['id'])
        return obj


class CreatePlayer(CreateView):
    context_object_name = 'Create'
    model = Player
    fields = ['name', 'description', 'picture', 'active']


class PlayerUpdate(UpdateView):
    context_object_name = 'Update'
    model = Player
    fields = ['name', 'description', 'picture', 'active']

    def get_object(self):
        obj = get_object_or_404(Player, id=self.kwargs['id'])
        return obj

    def get_context_data(self, **kwargs):
        context = super(PlayerUpdate, self).get_context_data(**kwargs)
        context['update_view'] = True
        return context


class PlayerDelete(DeleteView):
    model = Player
    success_url = reverse_lazy('PlayersManagement:PlayersList')

    def get_object(self):
        obj = get_object_or_404(Player, id=self.kwargs['id'])
        return obj

