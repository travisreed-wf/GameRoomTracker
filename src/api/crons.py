from flask.views import MethodView
from src.user.user import User


class MetricsCron(MethodView):

    def get(self):
        users = User.query().fetch()
        for user in users:
            user.update_pool_stats()


def setup_urls(app):
    app.add_url_rule(
        '/api/crons/metrics/',
        view_func=MetricsCron.as_view('api.crons.metrics'))
