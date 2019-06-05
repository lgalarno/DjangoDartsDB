from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse,JsonMinResponse

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
    # return StreamingHttpResponse(JsonResponse({'requestKey': secrets.token_hex(10).upper(), #'E173663A785B72C4D75E',
    #                          'activationCode': act_code, #'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
    #                          'expirationDate': d.strftime("%m/%d/%Y")
    #                          }), content_type='application/json')
    return JsonMinResponse({'requestKey': secrets.token_hex(10).upper(), #'E173663A785B72C4D75E',
                             'activationCode': act_code, #'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
                             'expirationDate': d.strftime("%m/%d/%Y")
                             })

# @api_view(['GET', 'POST'])
# def license_check2(request, act_code=None):
#     print(act_code)
#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world!"})