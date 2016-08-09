import flask
from google.appengine.api import users
from google.appengine.ext import ndb
import trueskill

from src.config import DEFAULT_RANK_ELASTICITY, DEFAULT_RANK_POINTS

class Rating(ndb.Model):
    elasticity = ndb.FloatProperty(default=DEFAULT_RANK_ELASTICITY)
    points = ndb.FloatProperty(default=DEFAULT_RANK_POINTS)

class User(ndb.Model):
    """
    Represents a user (player or observer) of the GameRoomTracker
    ID will equal the username that they originally used for sign in
    """
    email = ndb.StringProperty(required=True)
    experience = ndb.IntegerProperty(default=0)
    name = ndb.StringProperty(required=True)
    rating = ndb.StructuredProperty(Rating)

    @property
    def is_admin(self):
        return User.current_user_is_admin()

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
