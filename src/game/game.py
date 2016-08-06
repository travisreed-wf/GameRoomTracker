from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    """Represents a single instance of a Game"""
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    player_keys = ndb.KeyProperty(kind="User", repeated=True)
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
        game.players = [s.player for s in player_records]
        game.put()
        return game  #  TODO: Calculate winner

    def calculate_rank_points_changes(self):
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
                record_index += 1
                player = record.player
                points_earned = rating.mu - player.rank_data.points
                record.rank_points_earned = points_earned
                player.rank_data.points = rating.mu
                player.rank_data.elasticity = rating.sigma
                to_put.append(player)
        ndb.put_multi(to_put)
