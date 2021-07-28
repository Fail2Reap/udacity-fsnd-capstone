import os
import json
from functools import wraps

from flask import request, current_app
from jose import jwt
from urllib.request import urlopen


class AuthError(Exception):
    """A standardized way to communicate auth failure modes
    """

    def __init__(self, error: dict, status_code):
        """Class constructor.

        Args:
            error (json): [description]
            status_code ([type]): [description]
        """
        self.error = error
        self.status_code = status_code


def _get_token_auth_header():
    """Get a token from an Authorization header.

    Raises:
        AuthError: Auth header is missing.
        AuthError: Auth header must start with "Bearer".
        AuthError: Token not found.
        AuthError: Auth header not a Bearer token.

    Returns:
        str: A complete token without the "Bearer" prefix.
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]

    return token


def _verify_decode_jwt(token):
    """Verifies a JSON Web Token.

    Args:
        token (str): A JSON Web Token.

    Raises:
        AuthError: Auth header malformed.
        AuthError: Token expired.
        AuthError: Invalid claims.
        AuthError: Unable to parse Auth token.
        AuthError: Unable to find key.

    Returns:
        dict: Decoded JSON Web Token.
    """
    try:
        if current_app.config['TESTING']:
            return jwt.decode(
                token,
                os.environ.get('SIGNING_PUB_KEY'),
                audience=current_app.config['AUTH_API_AUDIENCE'],
                algorithms=current_app.config['AUTH_ALGORITHM']
            )
    except Exception:
        # Raised of the token is not a self-signed token
        pass

    jsonurl = urlopen(f"https://{current_app.config['AUTH_DOMAIN']}"
                      "/.well-known/jwks.json")
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
                algorithms=current_app.config['AUTH_ALGORITHM'],
                audience=current_app.config['AUTH_API_AUDIENCE'],
                issuer=f"https://{current_app.config['AUTH_DOMAIN']}/"
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
                'description': 'Incorrect claims. Please, check the audience '
                               'and issuer.'
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


def _check_permissions(permission, payload):
    """Checks whether the JSON Web Token contains valid and
    required permission.

    Args:
        permission (str): Required permission to access a resource.
        payload (dict): Decoded JWT.

    Raises:
        AuthError: Permissions not included in JWT.
        AuthError: Permissions not found in JWT.

    Returns:
        bool: True if claims are valid.
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = _get_token_auth_header()
            payload = _verify_decode_jwt(token)
            _check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
