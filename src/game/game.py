from google.appengine.ext import ndb
from google.appengine.ext.ndb import polymodel


class Game(polymodel.PolyModel):
    """Represents a single instance of a Game"""
    date = ndb.DateTimeProperty(auto_now_add=True, required=True)
    player_keys = ndb.KeyProperty(kind="User", repeated=True, required=True)
    player_record_keys = ndb.KeyProperty(
        kind="GamePlayerRecord", repeated=True, required=True)
    winner_keys = ndb.KeyProperty(kind="User", repeated=True)

    @staticmethod
    def _update_ranked_data(sorted_player_records, rated_rating_groups):
        to_put = [sorted_player_records]
        for team in rated_rating_groups:
            record_index = 0
            for rating in team.itervalues():
                record_index += 1
                record = sorted_player_records[record_index]
                player = record.player
                points_earned = rating.mu - player.rank_data.points
                record.rank_points_earned = points_earned
                player.rank_data.points = rating.mu
                player.rank_data.elasticity = rating.sigma
                to_put.append(player)
        ndb.put_multi(to_put)
