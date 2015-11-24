from mongoengine import *


class Years(EmbeddedDocument):
    start = IntField(required=True, min_value=0)
    end = IntField(min_value=0)


class Episode(EmbeddedDocument):
    id = IntField(unique=True, required=True)
    name = StringField(required=True, max_length=250)
    air_date = DateTimeField()


class Season(EmbeddedDocument):
    id = IntField(unique=True, required=True)
    episodes = ListField(Episode)


class Show(Document):
    tvdb_id = IntField(unique=True, required=True, min_value=0)
    name = StringField(required=True, max_length=250)
    years = EmbeddedDocumentField(Years)
    seasons = ListField(Season)


class User(Document):
    email = EmailField(unique=True)
    display_name = StringField(max_length=250)
    google = StringField(max_length=120, unique=True)
    shows = ListField(ReferenceField(Show))
