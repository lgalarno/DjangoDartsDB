from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.utils.encoding import  smart_str
from django.shortcuts import render, HttpResponseRedirect,HttpResponse, get_object_or_404, reverse

import zipfile
import datetime
import os
import csv

from .models import zipcsvfile
from .maketables import WriteTables, WriteScoreTables, Write_csv, CSV_to_db


def csvweb(request, category=None):
    if request.method == 'GET':
        if category in ['501','BB']:
            rtable, stable, headerrank,headersummary,maxplist = WriteTables(category)
        elif category == 'BBScores':
            rtable, stable, headerrank,headersummary,maxp = WriteScoreTables()
        else:
            messages.warning(request, "Nothing to do")
            return HttpResponseRedirect('/')
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(category)
        writer = csv.writer(response)
        writer.writerow(headerrank)
        writer.writerows(rtable)
        writer.writerows([''])
        writer.writerow(headersummary)
        writer.writerows(stable)
        writer.writerows([''])
        return response
    messages.warning(request, "Nothing to do")
    return HttpResponseRedirect('/')

def webtables(request, category=None):
    if request.method == 'GET':
        if category in ['501', 'BB']:
            rtable, stable, headerrank, headersummary, maxplist = WriteTables(category)
            stable_title = 'Standings'
        elif category == 'BBScores':
            rtable, stable, headerrank, headersummary, maxplist = WriteScoreTables()
            stable_title = 'Average scores'
        else:
            messages.warning(request, "Nothing to do")
            return HttpResponseRedirect('/')
        # if len(rtable)<1:
        #     messages.warning(request, "No {} games found.".format(tabletype))
        #     return HttpResponseRedirect('/'),
        context = {'title':'DartsTables{}'.format(category),
                   'maxplist': maxplist,
                   'headerrank':headerrank,
                   'headersummary':headersummary,
                   'maintable':rtable,
                   'summarytable':stable,
                   'stable_title': stable_title}
        return render(request, 'scoretable/table.html', context)
    else:
        messages.warning(request, "Nothing to do")
        return HttpResponseRedirect('/')

def csvzip(request):
    path =  os.path.join(settings.MEDIA_ROOT, 'files')
    print(path)
    datesuffix = datetime.datetime.now().strftime('_%Y_%m_%d')
    zipfilename = 'DartsTablesCSV' + datesuffix + '.zip'
    longzipfilename = os.path.join(path, zipfilename)
    try:
        zip_archive = zipfile.ZipFile(longzipfilename, 'w')

        for tabletype in ['501', 'BB']:
            rtable, stable, headerrank, headersummary, maxplist = WriteTables(tabletype)
            if len(rtable) > 0:
                outfile = 'DartsTables{}'.format(tabletype) + datesuffix + '.csv'
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
        context = {'title':'Download',
                   'allfiles':allfiles
                   }
        return render(request, 'scoretable/download.html', context)
    except:
        messages.warning(request, "Error making the csv files")
        return HttpResponseRedirect('/')

def downloadzip(request,filename=None):
    f = get_object_or_404(zipcsvfile, filename=filename)
    link = f.path
    response = HttpResponse()
    response['Content-Type']='application/zip'
    response['Content-Disposition'] = "attachment; filename='{}'".format(filename)
    response['X-Sendfile']= smart_str(link)
    f.timesdownloaded += 1
    f.save()
    return response

def deletezip(request,PK):
    print(PK)
    todel = get_object_or_404(zipcsvfile, id=PK )
    todel.path.delete()
    todel.delete()
    allfiles = zipcsvfile.objects.all().order_by("-timestamp")
    context = {'title': 'Download',
               'allfiles': allfiles
               }
    return render(request, 'scoretable/download.html', context)

def upload_csv(request):
    if request.method == "POST":
        csvfile = request.FILES['csvfile']
        if not csvfile.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("scoretable:upload_csv"))
        CSV_to_db(csvfile)
        messages.success(request, "It worked!")
        return HttpResponseRedirect('/')
    return render(request, 'scoretable/uploadcsv.html', {'title':'Upload'})