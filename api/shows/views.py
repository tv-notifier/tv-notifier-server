from mongoengine import DoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth.decorators import login_required
from api.models import Show
from .errors import InvalidShowId


@login_required
@api_view(('PUT',))
def follow(request, user, show_id):
    """API view for following TV Shows by users"""
    try:
        show = Show.objects.get(tvdb_id=show_id)
    except DoesNotExist:
        show = Show.from_api(int(show_id))
    except KeyError:
        return InvalidShowId()

    user.follow_show(show)
    return Response({
        'show': show.to_dict_short(),
        'followed': show in user.shows
    })
