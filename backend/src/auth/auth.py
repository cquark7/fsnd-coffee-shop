import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'deepankar.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is not None:
        bearer_token_list = auth_header.split(' ')
        if bearer_token_list[0] and bearer_token_list[0].lower() == 'bearer' and bearer_token_list[1]:
            return bearer_token_list[1]
    raise AuthError({
        'success': False,
        'message': 'JWT not found',
        'error': 401
    }, 401)


def check_permissions(permission, payload):
    if permission in payload.get('permissions', []):
        return True
    raise AuthError({
        'success': False,
        'message': 'Permission not found in JWT',
        'error': 401
    }, 401)


def verify_decode_jwt(token):
    # get public key
    jsonurl = urlopen(f'http://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # get data in header
    unverified_header = jwt.get_unverified_header(token)

    # choose key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'message': 'Authorization malformed',
            'error': 401,
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'message': 'Token expired',
                'error': 401,
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'message': 'Incorrect claims. Please, check the audience and issuer',
                'error': 401,
            }, 401)
        except Exception:
            raise AuthError({
                'success': False,
                'message': 'Unable to parse authentication token',
                'error': 400,
            }, 400)
    raise AuthError({
        'success': False,
        'message': 'Unable to find the appropriate key',
        'error': 400,
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
