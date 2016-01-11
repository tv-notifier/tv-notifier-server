"""Views used for authentication and authorization"""

import json

import requests
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from api.models import User
from .common import create_token
from .errors import AuthenticationError
from .serializers import GoogleAuthSerializer


@api_view(('POST',))
@parser_classes((JSONParser,))
def google(request):
    """API authentication using Google OAuth2"""
    serializer = GoogleAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    payload = {
        'client_id': serializer.validated_data['client_id'],
        'redirect_uri': serializer.validated_data['redirect_uri'],
        'client_secret': settings.GOOGLE_SECRET,
        'code': serializer.validated_data['code'],
        'grant_type': 'authorization_code'
    }

    # Step 1. Exchange authorization code for access token.
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    try:
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
    except KeyError:
        raise AuthenticationError(token['error'])

    # Step 2. Retrieve information about the current user.
    r = requests.get(userinfo_url, headers=headers)
    profile = json.loads(r.text)
    user = User.objects(google=profile['id']).first()
    if user:
        token = create_token(user)
        return Response({'token': token})

    u = User(email=profile['email'], google=profile['id'],
             display_name=profile['name'])
    u.save()
    token = create_token(u)
    return Response({'token': token})
