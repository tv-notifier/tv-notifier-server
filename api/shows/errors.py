from rest_framework import status
from rest_framework.exceptions import APIException


class InvalidShowId(APIException):
    """Error used when a particular tv show does not exist in the database"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Provided TV Show does not exist.'
