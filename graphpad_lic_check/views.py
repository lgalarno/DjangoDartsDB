from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, StreamingHttpResponse
import datetime
import json
import secrets

def license_check(request, act_code=None):
    """
    List all code snippets, or create a new snippet.
    """
    # print(request)
    # requestID = request.GET.get('requestID', '')
    # print(requestID)
    # print( act_code)
    d = datetime.date(2028,12,31)
    if request.method == 'GET':
        return StreamingHttpResponse(JsonResponse({'requestKey': secrets.token_hex(10).upper(), #'E173663A785B72C4D75E',
                                 'activationCode': act_code, #'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
                                 'expirationDate': d.strftime("%m/%d/%Y")
                                 }), content_type='application/json')
        # return JsonResponse({'requestKey': secrets.token_hex(10).upper(), #'E173663A785B72C4D75E',
        #                          'activationCode': act_code, #'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
        #                          'expirationDate': d.strftime("%m/%d/%Y")
        #                          })

    elif request.method == 'POST':
        pass

