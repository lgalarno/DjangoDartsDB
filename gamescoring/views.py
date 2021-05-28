from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.utils import timezone
from django.views.generic import CreateView
from django.views.decorators.http import require_POST
from PlayersManagement.models import Player

from django.db import transaction

from .backend import ranking
from .forms import Participant501FormSet,ParticipantBBFormSet
from .models import GameNumber,Participant


#get or post?
class NewScore(CreateView):
    model = GameNumber
    fields = []
    success_url = HttpResponse('success')

    def get_context_data(self, **kwargs):
        data = super(NewScore, self).get_context_data(**kwargs)
        if self.request.POST:
            data['participants'] = Participant501FormSet(self.request.POST)
        else:
            data['participants'] = Participant501FormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        participants = context['participants']
        with transaction.atomic():
            self.object = form.save()

            if participants.is_valid():
                participants.instance = self.object
                participants.save()
        return super(NewScore, self).form_valid(form)
    #return HttpResponse('Get Score')


#get or post?
def EnterScore(request,category=None):
    if category in ['BB','501']:
        players = Player.objects.filter(active=True)
        context = {'players': players,
                   'gamecategory':category}
        return render(request, 'gamescoring/EnterScore.html', context)
    else:
        messages.warning(request, "Nothing to do")
        return HttpResponseRedirect('/')


@require_POST
def ScoreConfirm(request):
    requestdict = dict(request.POST)
    selectp = requestdict.get('selectp')
    gamecategory = request.POST.get('gamecategory')
    if selectp:
        selectedplayers = Player.objects.filter(pk__in=selectp)
        pscore = requestdict.get('pscore')
        header = ['Player','rank']
        if gamecategory == 'BB':
            pranks = ranking(pscore)
            header.append('score')
        else:
            #restore proper naming of pranks and pscore for 501
            pranks = list(pscore)
            pscore = [None for i in range(len(pscore))]
        zipped = zip(selectedplayers, pranks, pscore)
        context = {
            'header':header,
            'zipped': zipped,
            'gamecategory': gamecategory
            }
        return render(request, 'gamescoring/ScoreConfirm.html', context)
    messages.warning(request, "No player(s) selected!")
    return HttpResponseRedirect('/')


@require_POST
def SaveScore(request):
    try:
        requestdict = dict(request.POST)
        category = request.POST.get('gamecategory')
        selectedplayers = requestdict.get('selectedp')
        pranks = requestdict.get('prank')
        if category == 'BB':
            pscores = requestdict.get('pscore')
        else:
            pscores = [None for i in range(len(pranks))]
        header = ['Player', 'rank']
        if category == 'BB':
            header.append('score')
        zipped = zip(selectedplayers, pranks, pscores)
        now = timezone.now()
        g = GameNumber(date= timezone.localdate(now),
                       time= timezone.localtime(now).time(),
                       gamenumber= GameNumber.objects.filter(category = category).count()+1,
                       category=category)
        g.save()
        for i in range(0,len(selectedplayers)):
            p = Player.objects.get(name=selectedplayers[i])
            s = Participant(game=g, rank=pranks[i], score=pscores[i],player=p)
            s.save()
        context = {
            "header":header,
            "zipped": zipped,
            "gameID":g.gamenumber,
            "date": g.date,
            "gamecategory":category
        }
        return render(request, 'gamescoring/ScoreSuccess.html', context)
    except:
        messages.warning(request, "Sorry, something wrong happened entering data in the database")
        return HttpResponseRedirect('/')
