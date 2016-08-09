from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    """Represents a single instance of a Game"""
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    player_keys = ndb.ComputedProperty(
        lambda self: self._player_keys, repeated=True)
    player_record_keys = ndb.KeyProperty(
        kind="GamePlayerRecord", repeated=True)
    winner_keys = ndb.ComputedProperty(
        lambda self: self._winner_keys, repeated=True)

    @property
    def player_records(self):
        if hasattr(self, "_player_records"):
            return self._player_records
        self._player_records = ndb.get_multi(self.player_record_keys)
        return self._player_records

    @property
    def _player_keys(self):
        """Dont use this, use ComputedProperty instead"""
        return [r.player_key for r in ndb.get_multi(self.player_record_keys)]

    @property
    def _winner_keys(self):
        """Dont use this, use ComputedProperty instead"""
        winner_keys = []
        for record in ndb.get_multi(self.player_record_keys):
            if record.player_placement == 1:
                winner_keys.append(record.player_key)
        return winner_keys

    @classmethod
    def add(cls, player_records):
        """
        Use a game type and a list of player records to add a Game to db
        :param player_records a list of GamePlayerRecords
        :returns: a game object
        """
        game = cls(player_record_keys=[r.key for r in player_records])
        game.calculate_experience()
        game.calculate_rating_change()
        game.players = [s.player for s in player_records]
        game.put()
        return game

    def calculate_rating_change(self):
        """
        Calculate points using self.player_records
        Should be overwritten by subclass
        """
        pass

    def calculate_experience(self):
        """
        Use self.player_records to assign experience to the relevant players
        """
        pass

    @staticmethod
    def _update_ranked_data(sorted_player_records, rated_rating_groups):
        to_put = sorted_player_records
        record_index = 0
        for team in rated_rating_groups:
            for rating in team.itervalues():
                record = sorted_player_records[record_index]
                player = record.player

                points_earned = rating.mu - player.rating.points
                record.rank_points_earned = points_earned
                player.update_rating(rating)
                to_put.append(player)

                record_index += 1
        ndb.put_multi(to_put)
