"""The auth module commons"""

from datetime import datetime, timedelta

import jwt
from django.conf import settings

from api.errors import InvalidRequestData


def create_token(user):
    payload = {
        'sub': str(user.id),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')


def parse_token(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION').split()[1]
    except IndexError:
        raise InvalidRequestData('Incomplete Authorization header.')

    return jwt.decode(token, settings.SECRET_KEY)
