from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class GamePlayerRecord(polymodel.PolyModel):
    """Represents a single instance of a Game Record"""
    player_key = ndb.KeyProperty(kind="User", required=True)
    player_placement = ndb.IntegerProperty(required=True,
                                           choices=[1, 2, 3, 4, 5])
    rank_points_earned = ndb.FloatProperty(default=0.0)

    @property
    def game(self):
        from src.game.game import Game
        return Game.query(Game.player_record_keys==self.key).get()

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

    @property
    def win_weight(self):
        """
        Determine how close you were to winning based upon placement
        Eightball is binary (0, 1) but CutThroat is more complicated
        CutThroat
        3 Players: 1, .50, 0
        4 Players: 1, .66, .33, 0
        5 Players: 1, .75, .50, .25, 0
        """
        game = self.game
        if game.__class__.__name__ == 'EightBallGame':
            if self.player_placement == 1:
                return 1.0
            else:
                return 0.0
        else:
            step_size = float(1) / (len(game.player_record_keys) - 1)
            penalty = (self.player_placement - 1) * step_size
            return 1.0 - penalty


