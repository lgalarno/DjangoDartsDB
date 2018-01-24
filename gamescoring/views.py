from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.http import require_POST
from PlayersManagement.models import Player

from .backend import ranking
from .models import GameNumber,Participant

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
