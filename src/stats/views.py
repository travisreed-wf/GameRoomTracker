from flask import render_template
from flask.views import MethodView

from src.user.user import User


class LeaderboardView(MethodView):

    def get(self):
        users = User.query().fetch()
        return render_template('leaderboard.html', users=users)


def setup_urls(app):
    app.add_url_rule(
        '/stats/leaderboard/',
        view_func=LeaderboardView.as_view('leaderboard'))
