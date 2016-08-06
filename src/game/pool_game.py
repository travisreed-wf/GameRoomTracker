from google.appengine.ext import ndb

from src.game.game import Game

class PoolGame(Game):
    """Represents a game of Pool"""
    final_state = ndb.StructuredProperty(kind=PlayerPoolBallsState,
                                         repeated=True)

    @classmethod
    def add(cls, final_state):
        """
        Use a game type and a final state to add a PoolGame to the datastore
        :param final_state: a list of PlayerBoolBallsStates
        :returns: a game object
        """
        game = cls(final_state=final_state)
        game.point_data = game.calculate_points()
        game.players = [s.player for s in final_state]
        game.put()
        return game  #  TODO: Calculate winner

    def calculate_points(self):
        """
        Calculate points using self.final_state
        Should be overwritten by subclass
        """
        pass

    def calculate_experience(self):
        """Use self.final_state to assign experience to the relevant players"""
        pass



class CutThroatGame(PoolGame):

    def calculate_points(self):
        """
        Calculate Points using the following formula
        A win is worth 5 points, second place is worth 2 points
        """
        pass  # TODO


class EightBallGame(PoolGame):

    def calculate_points(self):
        """
        Calculate Points using the following formula
        A win is worth 3 points
        """
        pass  # TODO

class PlayerPoolBallsState(ndb.StructuredProperty):
    """Represents a single players part of the final game state"""
    player_key = ndb.KeyProperty(kind="User")
    balls_remaining = ndb.IntegerProperty()

