import json
from datetime import datetime, timedelta

import requests
import jwt
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes

from rest_framework.response import Response

from rest_framework.parsers import JSONParser

from api.models import User
from api.serializers import GoogleAuthSerializer


def create_token(user):
    payload = {
        'sub': str(user.id),
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token.decode('unicode_escape')


@api_view(('POST',))
@parser_classes((JSONParser,))
def google(request):
    """
    Google OAuth2
    """
    serializer = GoogleAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = (
        'https://www.googleapis.com/plus/v1/people/me'
    )
    payload = {
        'client_id': serializer.validated_data['clientId'],
        'redirect_uri': serializer.validated_data['redirectUri'],
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
        # TODO(poxip): Implement errors
        return Response(token)

    # Step 2. Retrieve information about the current user.
    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)
    user = User.objects(google=profile['id']).first()
    if user:
        token = create_token(user)
        return Response({'token': token})

    u = User(google=profile['id'],
             display_name=profile['displayName'])
    u.save()
    token = create_token(u)
    return Response({'token': token})
