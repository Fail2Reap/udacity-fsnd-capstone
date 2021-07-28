import os

from flask import current_app
from jose import jwt

payloads = {
    'public': {
        'aud': 'wow-auctions',
        'permissions': []
    },
    'free': {
        'aud': 'wow-auctions',
        'permissions': [
            'get:auction',
            'get:item'
        ]
    },
    'premium': {
        'aud': 'wow-auctions',
        'permissions': [
            'get:auctions',
            'get:auction',
            'get:items',
            'get:item'
        ]
    },
    'admin': {
        'aud': 'wow-auctions',
        'permissions': [
            'get:auctions',
            'post:auctions',
            'get:auction',
            'patch:auction',
            'delete:auction',
            'get:items',
            'post:items',
            'get:item',
            'patch:item',
            'delete:item'
        ]
    }
}


def get_token(user: str) -> str:
    """Returns a valid JWT for testing purposes.

    Args:
        user (str): User to request token for.

    Returns:
        str: A JWT.
    """
    token = jwt.encode(
        payloads[user.lower()],
        os.environ.get('SIGNING_PRIV_KEY'),
        algorithm=current_app.config['AUTH_ALGORITHM']
    )

    return f'Bearer {token}'
