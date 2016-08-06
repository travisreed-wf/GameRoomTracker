from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    """Represents a single instance of a Game"""
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    player_keys = ndb.KeyProperty(kind="User", repeated=True, required=True)
    player_record_keys = ndb.KeyProperty(
        kind="GamePlayerRecord", repeated=True, required=True)
    winner_keys = ndb.KeyProperty(kind="User", repeated=True)
