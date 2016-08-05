from google.appengine.ext import ndb

from src.game.game import Game

class PoolGame(Game):
    final_state = ndb.StructuredProperty(PlayerPoolBallsState, repeated=True)

    @classmethod
    def create(cls, final_state):
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



class CutThroatGame(PoolGame):

    def calculate_points(self):
        pass  # TODO


class EightBallGame(PoolGame):
    pass

    def calculate_points(self):
        pass  # TODO

class PlayerPoolBallsState(ndb.StructuredProperty):
    player = ndb.KeyProperty("User")
    balls_remaining = ndb.IntegerProperty()

