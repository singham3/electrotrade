from rest_framework.authentication import get_authorization_header
from .models import *
import jwt
from datetime import datetime, timedelta

token_key = eval(open('/var/www/html/electonicswebservice/config/secret-key.json', 'r').read())


def user_token_authentication(request):
    auth = get_authorization_header(request).split()
    if not auth or auth[0].lower() != b'token': 
        return None

    if len(auth) == 1: 
        return {"Error": 'Invalid token header. No credentials provided.'}
    elif len(auth) > 2: 
        return {"Error": 'Invalid token header'}

    try: 
        token = auth[1]
        if token == "null": 
            return {"Error": "Null token not allowed"}
    except UnicodeError: 
        return {"Error": 'Invalid token header. Token string should not contain invalid characters.'}

    return authenticate_credentials(token)


def authenticate_credentials(token): 
    payload = jwt.decode(token, token_key["token_key"])
    account_id = payload['account_id']
    username = payload['username']
    token_created_at = payload['token_created_at']
    try: 
        # if datetime.now() - datetime.strptime(str(token_created_at), '%Y-%m-%d %H:%M:%S.%f') > timedelta(seconds=10):
        #     return {"Error": 'Token Time Out'}
        user = Register.objects.get(username=username, account_id=account_id)
        if not user.token == token.decode():
            return {"Error": 'Token Mismatch'}

    except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError: 
        return {"Error":  'Token is Expired'}
    except Register.DoesNotExist:
        return {"Error": 'Token is Invalid'}
    return user
