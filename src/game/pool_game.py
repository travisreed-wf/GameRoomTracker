from src.game.game import Game

class PoolGame(Game):
    """Represents a game of Pool"""

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
        pass  # TODO


class EightBallGame(PoolGame):

    def calculate_rank_points_changes(self):
        """
        Calculate Points using the following formula
        A win is worth 3 points
        """
        pass  # TODO
