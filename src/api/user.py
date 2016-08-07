import json

from flask.views import MethodView
from src.user.user import User


class Usernames(MethodView):

    def get(self):
        users = User.query().fetch()
        names = [u.name for u in users]
        return json.dumps(names), 200


def setup_urls(app):
    app.add_url_rule(
        '/api/user/usernames/',
        view_func=Usernames.as_view('api.user.usernames'))
