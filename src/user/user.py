import flask
from google.appengine.api import users
from google.appengine.ext import ndb


class User(ndb.Model):
    """
    Represents a user (player or observer) of the GameRoomTracker
    ID will equal the username that they originally used for sign in
    """
    display_name = ndb.StringProperty()
    email = ndb.StringProperty(required=True)
    experience = ndb.IntegerProperty()
    total_points = ndb.IntegerProperty()

    @property
    def is_admin(self):
        return User.current_user_is_admin()

    @property
    def games_played(self):
        # Query game.players
        return 0

    @property
    def games_won(self):
        # Query Game.winners
        return 0

    @property
    def level(self):
        return 1

    @property
    def win_percentage(self):
        # self.games_won / self.games_played
        games_played = self.games_played
        if games_played:
            return self.games_won / self.games_played
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
        display_name = username.replace('.', ' ').title()
        user = User(id=username, email=email, display_name=display_name)
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
            'display_name': self.display_name,
            'email': self.email,
            'is_admin': self.is_admin,
        }
        flask.session['user'] = user_data
