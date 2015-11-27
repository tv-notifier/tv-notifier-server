"""File containing our own error classes and default exception handler"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import (
    APIException, ValidationError, NotFound, PermissionDenied
)
from rest_framework.views import exception_handler as default_exception_handler


def exception_handler(exc, context):
    """Default exception handler

    Extends the functionality of REST Framework exception handler
    (:py:func:`rest_framework.views.exception_handler`) by adding statusCode
    field, name of the error and cleaning up ValidationError response data.
    """
    response = default_exception_handler(exc, context)

    if response is not None:
        name = exc.__class__.__name__
        if isinstance(exc, ValidationError):
            response.data = {'fields': response.data}
            # ValidationError is renamed to InvalidRequestData, although these
            # two errors are not the same
            name = 'InvalidRequestData'
        response.data['name'] = name
        response.data['statusCode'] = response.status_code

    return response


def url_exception_handler(exception):
    """Get urls.py exception handler for given exception.

    :param exception: exception to handle
    :return: handler function
    """

    @api_view(('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'TRACE'))
    def view(request, exc):
        """Simple API view which raises given error

        This view is used in URL exception handlers. The error is handled by
        default exception handler, and therefore the response is generated.

        :param Exception exc: exception to handle
        :return: Response object
        :rtype: rest_framework.response.Response
        """
        raise exc

    def handler(request):
        """View that returns response from the error handler as a HttpResponse

        :type request: django.http.HttpRequest
        :return: HttpResponse object
        :rtype: django.http.HttpResponse
        """
        response = view(request, exception)
        # We should not return Allow header
        del response['allow']
        return response.render()

    return handler


class BadRequest(APIException):
    """HTTP error 400"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request.'


class InternalServerError(APIException):
    """HTTP error 500"""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Internal Server Error.'


handler400 = url_exception_handler(BadRequest())
handler403 = url_exception_handler(PermissionDenied())
handler404 = url_exception_handler(NotFound())
handler500 = url_exception_handler(InternalServerError())
url_exception_handlers = handler400, handler403, handler404, handler500
"""Errors used in views"""


class InvalidShowId(APIException):
    """Error used when a particular tv show does not exist in the database"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Provided TV Show does not exist.'


class AuthenticationError(APIException):
    """Used when an error occurred during user authentication"""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred during the authentication process.'


class AuthorizationError(APIException):
    """Thrown when an error occurred during resource authorization"""
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'An error occurred during authorization.'


class InvalidRequestData(APIException):
    """Error thrown when the data sent in the request is invalid"""
    status_code = status.HTTP_400_BAD_REQUEST
