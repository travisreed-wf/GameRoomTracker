from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    date = ndb.DateTimeProperty(auto_now_add=True)
    player_keys = ndb.KeyProperty(kind="User", repeated=True)
    point_data = ndb.StructuredProperty(PointData, repeated=True)
    winner_keys = ndb.KeyProperty(king="User", repeated=True)


class PointData(ndb.StructuredProperty):
    player_key = ndb.KeyProperty(kind="User")
    points = ndb.IntegerProperty()
