from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class GamePlayerRecord(polymodel.PolyModel):
    """Represents a single instance of a Game Record"""
    player_key = ndb.KeyProperty(kind="User", required=True)
    player_placement = ndb.IntegerProperty(required=True,
                                           choices=[1, 2, 3, 4, 5])
    rank_points_earned = ndb.FloatProperty(default=0.0)

    @property
    def player(self):
        if hasattr(self, "_player"):
            return self._player
        self._player = self.player_key.get()
        return self._player


class PoolPlayerRecord(GamePlayerRecord):
    """Represents a single players part of the final game state"""
    balls_hit_in = ndb.IntegerProperty()
    balls_remaining = ndb.IntegerProperty()
    lag_rank = ndb.IntegerProperty(choices=[1, 2, 3, 4, 5])
    scratch_count = ndb.IntegerProperty()
