from datetime import datetime

from mongoengine import *

from api import tv


def parse_date(date):
    """Parse YYYY-DD-MM date to a Python datetime.datetime() object

    :param date str - The string containing the date to parse.
    :return datetime.datetime
    """
    return datetime.strptime('2015-31-01', '%Y-%d-%m')


class Episode(EmbeddedDocument):
    id = IntField(unique=True)
    name = StringField(required=True, max_length=250)
    air_date = DateTimeField()

    @classmethod
    def from_api_object(cls, episode):
        """Construct an Episode object from a TVDb episode object

        :param episode tvdb_api.Episode - The object to construct
            an Episode object from.
        """
        # The id (order in the season) has to be added manually
        return cls(name=episode['episodename'],
                   air_date=parse_date(episode['firstaired']))


class Season(EmbeddedDocument):
    id = IntField(unique=True, required=True)
    episodes = EmbeddedDocumentListField(Episode)

    @classmethod
    def from_api_object(cls, season, season_id=0):
        """Construct a Season object from a TVDb season object

        :param season tvdb_api.Season - The object to construct a Season from.
        :param season_id int - The season order number in a Show
            (starting from 1, 0 is reserved for Show extras)
        """
        return cls(id=season_id, episodes=[
            Episode.from_api_object(e) for e in season.values()
        ])


class Show(Document):
    tvdb_id = IntField(unique=True, required=True, min_value=0)
    name = StringField(required=True, max_length=250)
    year = IntField(min_value=0)
    seasons = EmbeddedDocumentListField(Season)

    @classmethod
    def from_api(cls, tvdb_id):
        """Create a Show object from TVDb

        :param tvdb_id int - The show's id fetch data from The TV Database.
        """
        api_show = tv[tvdb_id]
        show = cls(tvdb_id=api_show['id'], name=api_show['seriesname'],
                   year=parse_date(api_show['firstaired']).year)
        for season_id, season in enumerate(api_show.values()):
            show.seasons.append(Season.from_api_object(season, season_id))

        return show

    def to_dict_short(self):
        """Custom method to return only selected elements of a Show object.

        Use Show.to_mongo() to get the whole Show's info

        :return dict
        """
        return {
            'tvdb_id': self.tvdb_id,
            'name': self.name,
            'year': self.year,
        }


class User(Document):
    email = EmailField(unique=True)
    display_name = StringField(max_length=250)
    google = StringField(max_length=120, unique=True)
    shows = ListField(ReferenceField(Show))

    def is_following(self, show):
        self.reload()
        return show in self.shows

    def follow_show(self, show):
        """Follow a Show

        :param show Show - The TV show to follow.
        """
        self.update(add_to_set__shows=[show])
