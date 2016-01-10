from rest_framework import status
from rest_framework.exceptions import APIException


class AuthenticationError(APIException):
    """Used when an error occurred during user authentication"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred during the authentication process.'


class AuthorizationError(APIException):
    """Thrown when an error occurred during resource authorization"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'An error occurred during authorization.'
