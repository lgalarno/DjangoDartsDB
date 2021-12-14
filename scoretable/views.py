from django.conf import settings
from django.contrib import messages
from django.utils.encoding import smart_str
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404, redirect, reverse

import zipfile
import datetime
import os
import csv

from gamescoring.models import GameNumber, Participant
from gamescoring.backend import ranking
from .models import zipcsvfile
from .maketables import WriteTables, WriteScoreTables, Write_csv, CSV_to_db


def csvweb(request, category=None):
    if category in ['501','BB']:
        rtable, stable, headerrank,headersummary,maxplist = WriteTables(category)
    elif category == 'BBScores':
        rtable, stable, headerrank,headersummary,maxp = WriteScoreTables()
    else:
        messages.warning(request, "Nothing to do")
        return HttpResponseRedirect('/')
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{category}.csv"'
    writer = csv.writer(response)
    writer.writerow(headerrank)
    writer.writerows(rtable.values())
    writer.writerows([''])
    writer.writerow(headersummary)
    writer.writerows(stable)
    writer.writerows([''])
    return response


def webtables(request, category=None):
    if category in ['501', 'BB']:
        rtable, stable, headerrank, headersummary, maxplist = WriteTables(category)
        stable_title = 'Standings'
    elif category == 'BBScores':
        rtable, stable, headerrank, headersummary, maxplist = WriteScoreTables()
        stable_title = 'Average scores'
    else:
        messages.warning(request, "Nothing to do")
        return HttpResponseRedirect('/')
    context = {'title':f'Tables {category}',
               'maxplist': maxplist,
               'headerrank':headerrank,
               'headersummary':headersummary,
               'maintable':rtable,
               'summarytable':stable,
               'stable_title': stable_title}
    return render(request, 'scoretable/table.html', context)


def csvzip(request):
    path =  os.path.join(settings.MEDIA_ROOT, 'files')
    datesuffix = datetime.datetime.now().strftime('_%Y_%m_%d')
    zipfilename = 'DartsTablesCSV' + datesuffix + '.zip'
    longzipfilename = os.path.join(path, zipfilename)
    # try:
    if datesuffix:
        zip_archive = zipfile.ZipFile(longzipfilename, 'w')

        for tabletype in ['501', 'BB']:
            rtable, stable, headerrank, headersummary, maxplist = WriteTables(tabletype)
            if len(rtable) > 0:
                outfile = f'DartsTables{tabletype}' + datesuffix + '.csv'
                mf = Write_csv(headerrank, rtable, headersummary, stable)
                zip_archive.writestr(outfile, mf.read())
        if len(rtable) > 0:
            sbb, ssbb, headerscore, headersumscore, maxp = WriteScoreTables()
            outfile = 'DartsTablesBBScores' + datesuffix + '.csv'
            mf = Write_csv(headerscore, sbb, headersumscore, ssbb)
            zip_archive.writestr(outfile, mf.read())
        zip_archive.close()
        z, created = zipcsvfile.objects.get_or_create(filename=zipfilename)
        z.path = smart_str(longzipfilename)
        z.filename = zipfilename
        z.timesdownloaded = 0
        z.save()
        allfiles = zipcsvfile.objects.all()
        context = {'title': 'Download',
                   'allfiles': allfiles
                   }
        return render(request, 'scoretable/download.html', context)
    # except:
    #     messages.warning(request, "Error making the csv files")
    #     return HttpResponseRedirect('/')


def downloadzip(request, slug=None):
    f = get_object_or_404(zipcsvfile, slug=slug)
    link = f.path
    response = HttpResponse()
    response['Content-Type'] = 'application/zip'
    response['Content-Disposition'] = f"attachment; filename = '{f.filename}'"
    response['X-Sendfile'] = smart_str(link)
    f.timesdownloaded += 1
    f.save()
    return response


def editgame(request, id):
    if request.method == "GET":
        q = get_object_or_404(GameNumber, id=id )
        # category = q.category
        # players = q.get_all_players()

        context = {'title': 'Edit',
                   'game': q}
        return render(request, 'scoretable/edit.html', context)
    if request.method == "POST":
        g = get_object_or_404(GameNumber, id=id)
        try:
            requestdict = dict(request.POST)
            selectedplayers = requestdict.get('selectp')
            todb = dict.fromkeys(requestdict.get('selectp'))
            if g.category == 'BB':
                pscores = requestdict.get('pscore')
                pranks = ranking(pscores)
            else:
                pranks = requestdict.get('prank')
                pscores = [None for i in range(len(pranks))]
            z = zip(selectedplayers,pranks,pscores)
            todb = {p:{'rank':int(r),'score':int(s)} for p,r,s in z}
            for p in g.participant_set.all():
                if p.rank != todb[p.player.name]['rank']:
                    q = Participant.objects.get(game=g, player=p.player)
                    q.rank =  todb[p.player.name]['rank']
                    q.save()
                if p.score != todb[p.player.name]['score']:
                    q = Participant.objects.get(game=g, player=p.player)
                    q.score =  todb[p.player.name]['score']
                    q.save()
            return redirect('scoretable:editgame', id=g.id)
        except:
            messages.warning(request, "Sorry, something wrong happened entering data in the database")
            return HttpResponseRedirect('/')


def deletegame(request,id):
    q = get_object_or_404(GameNumber, id=id )
    gcat = q.category
    #todel.delete()
    return HttpResponseRedirect(reverse("scoretable:webtables", kwargs={'category':gcat}))


def deletezip(request,id):
    q = get_object_or_404(zipcsvfile, id=id )
    q.path.delete()
    q.delete()
    qs = zipcsvfile.objects.all().order_by("-timestamp")
    context = {'title': 'Download',
               'allfiles': qs
               }
    return render(request, 'scoretable/download.html', context)


def upload_csv(request):
    if request.method == "POST":
        csvfile = request.FILES['csvfile']
        if not csvfile.name.endswith('.csv'):
            messages.error(request, 'File is not CSV')
            return HttpResponseRedirect(reverse("scoretable:upload_csv"))
        if CSV_to_db(csvfile):
            messages.success(request, "It worked!")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Something wrong happened. Better check the database...")
    return render(request, 'scoretable/uploadcsv.html', {'title': 'Upload'})
