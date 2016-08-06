from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    """Represents a single instance of a Game"""
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    player_keys = ndb.KeyProperty(kind="User", repeated=True,)
    player_record_keys = ndb.KeyProperty(
        kind="GamePlayerRecord", repeated=True)
    winner_keys = ndb.KeyProperty(kind="User", repeated=True)

    @classmethod
    def add(cls, player_records):
        """
        Use a game type and a list of player records to add a Game to db
        :param player_records a list of GamePlayerRecords
        :returns: a game object
        """
        game = cls(player_record_keys=[r.key for r in player_records])
        game.calculate_experience()
        game.calculate_rank_points_changes()
        game.player_keys = [s.player_key for s in player_records]
        game.put()
        return game  #  TODO: Calculate winner
