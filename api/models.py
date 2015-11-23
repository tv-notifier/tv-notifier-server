from mongoengine import *


class User(Document):
    # TODO(poxip): Improve the User model
    email = EmailField(unique=True)
    google = StringField(max_length=120, unique=True)

    display_name = StringField(max_length=250)
