from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    date = ndb.DateTimeProperty(auto_now_add=True)
    players = ndb.KeyProperty("User", repeated=True)
    point_data = ndb.StructuredProperty(PointData, repeated=True)
    winners = ndb.KeyProperty("User", repeated=True)


class PlayerPoolBallsState(ndb.StructuredProperty):
    player = ndb.KeyProperty("User")
    balls_remaining = ndb.IntegerProperty()


class PointData(ndb.StructuredProperty):
    player = ndb.KeyProperty("User")
    points = ndb.IntegerProperty()


class PoolGame(Game):
    final_state = ndb.StructuredProperty(PlayerPoolBallsState, repeated=True)


class CutThroatGame(PoolGame):
    pass


class EightBallGame(PoolGame):
    pass
