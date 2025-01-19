from flask import request, abort
import requests
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401, 'Token is missing')
        response = requests.post('https://oauth-server/validate', data={'token': token})
        if response.status_code != 200:
            abort(401, 'Invalid token')
        return f(*args, **kwargs)
    return decorated
