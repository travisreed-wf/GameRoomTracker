from google.appengine.ext import ndb
from trueskill import Rating, TrueSkill

from src.config import DEFAULT_RANK_ELASTICITY, DEFAULT_RANK_POINTS
from src.game.game import Game


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



class CutThroatGame(PoolGame):

    def calculate_rank_points_changes(self):
        """
        Calculate Points using the following formula
        A win is worth 5 points, second place is worth 2 points
        """
        player_records = ndb.get_multi(self.player_record_keys)
        player_records = sorted(
            player_records, key=lambda r: r.player_placement)
        teams = [{r.player.name: r.player.rating} for r in player_records]

        ranks = [r.player_placement for r in player_records]

        env = TrueSkill(
            mu=DEFAULT_RANK_POINTS, sigma=DEFAULT_RANK_ELASTICITY,
            draw_probability=0.0)
        rated_rating_groups = env.rate(teams, ranks=ranks)
        self._update_ranked_data(player_records, rated_rating_groups)


class EightBallGame(PoolGame):

    def calculate_rank_points_changes(self):
        """
        Calculate Points using the following formula
        A win is worth 3 points
        """
        player_records = ndb.get_multi(self.player_record_keys)
        team1 = [r for r in player_records if r.player_placement == 1]
        team2 = [r for r in player_records if r.player_placement == 2]
        player_records = sorted(
            player_records, key=lambda r: r.player_placement)
        teams = []
        for team_records in [team1, team2]:
            team = {}
            for record in team_records:
                team[record.player.name] = record.player.rating
            teams.append(team)

        ranks = [0, 1]

        env = TrueSkill(
            mu=DEFAULT_RANK_POINTS, sigma=DEFAULT_RANK_ELASTICITY,
            draw_probability=0.0)
        rated_rating_groups = env.rate(teams, ranks=ranks)
        self._update_ranked_data(player_records, rated_rating_groups)
