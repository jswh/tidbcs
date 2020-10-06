import json
from flask import Response

def json_response(code, msg, data=''):
    resp = {
        'msg': msg,
        'data': data
    }
    return Response(json.dumps(resp), status=code, mimetype='application/json;charset=utf-8', )
