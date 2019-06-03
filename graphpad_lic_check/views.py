from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import secrets

def license_check(request, act_code=None):
    """
    List all code snippets, or create a new snippet.
    """
    # print(request)
    # requestID = request.GET.get('requestID', '')
    # print(requestID)
    # print( act_code)

    if request.method == 'GET':
        response = JsonResponse({'requestKey': secrets.token_hex(10).upper(), #'E173663A785B72C4D75E',
                                 'activationCode': act_code, #'ACTGP-8C8246DA-DC2899AB-A2983DB6-052A6C01',
                                 'expirationDate': '12/31/2028'
                                 }, safe=False)

        return response

    elif request.method == 'POST':
        pass

