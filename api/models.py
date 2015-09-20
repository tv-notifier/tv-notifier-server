from mongoengine import *


class HelloWorld(Document):
    count = IntField()
