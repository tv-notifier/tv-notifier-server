from mongoengine import DoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.auth.decorators import login_required
from api.models import Show
from .errors import InvalidShowId


def get_show(show_id):
    """Get a show from the database

    Returns a show from the database, fetches it if does not exist.
    :param show_id int - The TVDB id of the show to get.
    :returns Show
    """
    try:
        show = Show.objects.get(tvdb_id=show_id)
    except DoesNotExist:
        try:
            show = Show.from_api(int(show_id))
        except KeyError:
            raise InvalidShowId()

    return show

@login_required
@api_view(('PUT',))
def follow(request, user, show_id):
    """API view for following TV Shows by users"""
    show = get_show(show_id)
    user.follow_show(show)
    return Response({
        'show': show.to_dict_short(),
        'followed': show in user.shows
    })


@login_required
@api_view(('GET',))
def info(request, user, show_id):
    """API view for getting Show's data

    Includes whether the show is being followed by the user.
    """
    show = get_show(show_id)
    return Response({
        'show': show.to_mongo(),
        'followed': show in user.shows
    })
