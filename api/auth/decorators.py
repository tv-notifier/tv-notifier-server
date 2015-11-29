"""Authentication and authorization decorators"""

from functools import wraps
from jwt import DecodeError, ExpiredSignature

from api.models import User
from api.auth.common import parse_token
from api.errors import AuthorizationError, InvalidRequestData


def login_required(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if not request.META.get('HTTP_AUTHORIZATION'):
            raise InvalidRequestData('Missing Authorization header.')

        try:
            payload = parse_token(request)
        except DecodeError:
            raise AuthorizationError('Token is invalid.')
        except ExpiredSignature:
            raise AuthorizationError('Token has expired.')

        user = User.objects.get(id=payload['sub'])
        return f(request, user, *args, **kwargs)

    return decorated_function
