from flask import render_template
from flask.views import MethodView

from src.user.user import User


class HomeView(MethodView):

    def get(self):
        users = User.query().fetch()
        return render_template('home.html', users=users)


def setup_urls(app):
    app.add_url_rule('/', view_func=HomeView.as_view('home'))
