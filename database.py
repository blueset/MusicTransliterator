import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Music(db.Document):
    file = db.StringField()
    last_update = db.DateTimeField(default=datetime.datetime.now)
    last_scan = db.DateTimeField(default=datetime.datetime.now)
    title = db.StringField()
    artist = db.StringField()
    album = db.StringField(default="")
    title_key = db.StringField(default="")
    artist_key = db.StringField(default="")
    album_key = db.StringField(default="")
    reviewed = db.BooleanField(default=False)
