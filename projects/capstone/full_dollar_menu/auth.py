import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

# https://chris-campos.us.auth0.com/authorize?audience=
# coffee&response_type=token&client_id=M7Z7hlMKty4pbkgwQOLacIzoMDGqDcXX&
# redirect_uri=http://localhost:5000/
AUTH0_DOMAIN = 'chris-campos.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fdm'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
"""
Gets the authentication header from the bearer token.
"""


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Token was not provided'
        }, 401)
    auth_header = request.headers['Authorization']
    headers_parts = auth_header.split(' ')

    if len(headers_parts) != 2:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Token does not have only 2 parts.'
        }, 401)
    elif headers_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Not a bearer token'
        }, 401)
    return headers_parts[1]


"""
Checks to see if the given permission is within
the given payload from a bearer token.
"""


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
            }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 401)
    return True


"""
Decodes the jwt and verifies it to see if it
is an authenticated user with the Auth0 jwks.
"""


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
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
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


"""
Creates a wrapper function to verify authenticity as well
as permission access.
"""


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            if not check_permissions(permission, payload):
                abort(401)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator

