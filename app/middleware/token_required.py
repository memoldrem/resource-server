import requests
from functools import wraps
from flask import request, abort
from dotenv import load_dotenv
import os

load_dotenv()
VALIDATION_ENDPOINT = os.getenv("VALIDATION_ENDPOINT")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Retrieve the access token from the Authorization header or cookies
        token = request.cookies.get('access_token') or request.headers.get('Authorization')

        if not token:
            abort(401, 'Token is missing')

        
        try: # Send the token to the Express server for validation
            response = requests.post(
                VALIDATION_ENDPOINT,  
                json={'access_token': token},  # Sending the access token as JSON in the body
                cookies=request.cookies  # Send any existing cookies (if needed for refresh)
            )

            if response.status_code == 200:  # Token is valid, pass the request to the next handler
                return f(*args, **kwargs)
            else:
                abort(401, 'Invalid or expired token') # maybe we could just log out instead tho
        except requests.exceptions.RequestException as e:
            print(f"Error contacting the validation server: {e}")
            abort(500, 'Internal server error while validating token')

    return decorated
