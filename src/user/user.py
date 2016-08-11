import flask
from google.appengine.api import users
from google.appengine.ext import ndb
import trueskill

from src.config import DEFAULT_RANK_ELASTICITY, DEFAULT_RANK_POINTS
from src.helpers import mean

class Rating(ndb.Model):
    elasticity = ndb.FloatProperty(default=DEFAULT_RANK_ELASTICITY)
    points = ndb.FloatProperty(default=DEFAULT_RANK_POINTS)

class PoolStats(ndb.Model):
    average_lag_rank = ndb.FloatProperty()
    games_lost = ndb.IntegerProperty()
    games_played = ndb.IntegerProperty()
    games_won = ndb.IntegerProperty()
    total_balls_hit_in = ndb.IntegerProperty()
    total_scratches = ndb.IntegerProperty()
    weighted_win_percentage = ndb.FloatProperty()

    @property
    def average_balls_hit_in(self):
        return float(self.games_played) / self.total_balls_hit_in

    @property
    def average_scratches(self):
        return float(self.games_played) / self.total_scratches


class User(ndb.Model):
    """
    Represents a user (player or observer) of the GameRoomTracker
    ID will equal the username that they originally used for sign in
    """
    email = ndb.StringProperty(required=True)
    experience = ndb.IntegerProperty(default=0)
    name = ndb.StringProperty(required=True)
    pool_stats = ndb.StructuredProperty(PoolStats)
    rating = ndb.StructuredProperty(Rating)

    @property
    def is_admin(self):
        return User.current_user_is_admin()

    @property
    def games_played(self):
        from src.game.game import Game
        return Game.query(Game.player_record_keys==self.key).fetch()

    @property
    def games_played_count(self):
        # Query game.players
        return 0

    @property
    def games_won_count(self):
        # Query Game.winners
        return 0

    @property
    def level(self):
        return 1

    @property
    def pool_games_played(self):
        from src.game.pool_game import PoolGame
        return PoolGame.query(PoolGame.player_keys == self.key).fetch()

    @property
    def trueskill_rating(self):
        if not self.rating:
            self.rating = Rating()
            self.put()
        return trueskill.Rating(
            mu=self.rating.points, sigma=self.rating.elasticity)

    @property
    def win_percentage(self):
        # self.games_won / self.games_played
        games_played_count = self.games_played_count
        if games_played_count:
            return self.games_won_count / games_played_count
        else:
            return 0

    @staticmethod
    def add_or_get(email):
        """
        Creates or gets a user obj from User.email.
        If User does not exists, the User obj is created using the username as
        the key.id (which will persist even if User.username is changed).

        :param email: user's email address
        :type email: str
        :return: User obj
        :rtype: User obj
        """
        user = User.query(User.email == email).get()
        if user:
            return user
        username = email.split('@')[0]
        name = username.replace('.', ' ').title()
        user = User(id=username, email=email, name=name)
        user.put()
        return user

    @staticmethod
    def current_user():
        google_user = users.get_current_user()
        if google_user:
            return User.query(User.email == google_user.email()).get()
        return None

    @staticmethod
    def current_user_is_admin():
        return users.is_current_user_admin()

    @staticmethod
    def get_current_user_from_request(request):
        user = User.current_user()

        if not user and request.authorization:
            auth = request.authorization
            user = User.get_by_id(auth.username)
        return user

    def add_to_session(self):
        user_data = {
            'email': self.email,
            'is_admin': self.is_admin,
            'name': self.name,
        }
        flask.session['user'] = user_data

    def update_rating(self, trueskill_rating):
        self.rating.points = trueskill_rating.mu
        self.rating.elasticity = trueskill_rating.sigma

    def update_pool_stats(self):
        total_losses = 0
        total_wins = 0
        total_scratches = 0
        total_balls_hit_in = 0
        lag_ranks = []
        win_weights = []
        games = self.pool_games_played
        for game in games:
            record = game.get_player_record(self)

            if record.lag_rank:
                lag_ranks.append(record.lag_rank)

            win_weights.append(record.win_weight)
            if record.player_placement == 1:
                total_wins += 1
            else:
                total_losses += 1

            if record.scratch_count:
                total_scratches += record.scratch_count

            if record.balls_hit_in:
                total_balls_hit_in += record.balls_hit_in

        if not self.pool_stats:
            self.pool_stats = PoolStats()

        self.pool_stats.average_lag_rank = mean(lag_ranks)
        self.pool_stats.games_lost = total_losses
        self.pool_stats.games_won = total_wins
        self.pool_stats.games_played = total_wins + total_losses
        self.pool_stats.total_scratches = total_scratches
        self.pool_stats.total_balls_hit_in = total_balls_hit_in
        self.pool_stats._weighted_win_percentage = mean(win_weights)
        self.put()
