

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

import json
import datetime
import hashlib

class JsonMinResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.

    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before EcmaScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be a json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    :param json_dumps_params: A dictionary of kwargs passed to json.dumps().
    """
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data =  json.dumps(data, separators = (',', ':'), cls=encoder)   #json.dumps(data, separators = (',', ':')), cls=encoder)
        super(JsonMinResponse, self).__init__(content=data, **kwargs)


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

