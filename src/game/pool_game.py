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
        pass

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
