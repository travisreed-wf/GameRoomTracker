from google.appengine.ext import ndb
from trueskill import TrueSkill

from src.config import DEFAULT_RANK_ELASTICITY, DEFAULT_RANK_POINTS
from src.game.game import Game


class PoolGame(Game):
    """Represents a game of Pool"""


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
