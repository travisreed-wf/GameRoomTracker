from src.config import DEFAULT_RANK_ELASTICITY, DEFAULT_RANK_POINTS
from src.game.game import Game

from trueskill import Rating, TrueSkill

class PoolGame(Game):
    """Represents a game of Pool"""

    @classmethod
    def add(cls, player_records):
        """
        Use a game type and a list of player records to add a PoolGame to db
        :param player_records a list of PoolPlayerRecords
        :returns: a game object
        """
        game = cls(player_records=[r.key for r in player_records])
        game.calculate_experience(player_records)
        game.calculate_rank_points_changes(player_records)
        game.players = [s.player for s in player_records]
        game.put()
        return game  #  TODO: Calculate winner

    def calculate_rank_points_changes(self, player_records):
        """
        Calculate points using self.player_records
        Should be overwritten by subclass
        """
        player_records = sorted(
            player_records, key=lambda r: r.player_placement)
        rating_groups = [{p: p.player.rating_data} for p in player_records]

        ranks = [r.player_placement for r in player_records]

        env = TrueSkill(mu=DEFAULT_RANK_POINTS, sigma=DEFAULT_RANK_ELASTICITY,
                draw_probability=0.0)
        rated_rating_groups = env.rate(rating_groups, ranks=ranks)


    def calculate_experience(self, player_records):
        """
        Use self.player_records to assign experience to the relevant players
        """
        pass



class CutThroatGame(PoolGame):

    def calculate_rank_points_changes(self, player_records):
        """
        Calculate Points using the following formula
        A win is worth 5 points, second place is worth 2 points
        """
        pass  # TODO


class EightBallGame(PoolGame):

    def calculate_rank_points_changes(self, player_records):
        """
        Calculate Points using the following formula
        A win is worth 3 points
        """
        pass  # TODO
