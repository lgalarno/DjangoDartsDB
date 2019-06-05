from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse,JsonMinResponse

import datetime
import hashlib



def license_check(request, act_code=None):
    """
    List all code snippets, or create a new snippet.
    """
    # print(request)
    tohash = act_code+request.GET.get('requestID', '')+"kWNVrSrMHfH4KpIVcs8bSheLs4M"
    rk = hashlib.md5(tohash.encode('utf-8')).hexdigest().upper()
    d = datetime.date(2028,12,31)

    return JsonMinResponse({'requestKey': rk[0:20], #'E173663A785B72C4D75E',
                             'activationCode': act_code, #'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
                             'expirationDate': d.strftime("%m/%d/%Y")
                             })

