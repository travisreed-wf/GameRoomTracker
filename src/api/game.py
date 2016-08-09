from flask import request
from flask.views import MethodView
from google.appengine.ext import ndb

from src.game.game_player_record import PoolPlayerRecord
from src.game.pool_game import CutThroatGame, EightBallGame
from src.user.user import User


class GameAPI(MethodView):

    def post(self):
        data = request.get_json()
        if not self._is_valid_data(data):
            return 'Bad Request', 400

        game = self._get_class(data['game_type'])
        if not game:
            return 'Invalid game_type', 400

        records = self._create_records(data['players'])

        game.add(records)
        return 'Success', 200

    @staticmethod
    def _get_class(name_to_parse):
        cls = None
        if name_to_parse == 'Pool - Cut throat':
            cls = CutThroatGame
        elif name_to_parse == 'Pool - Eight ball':
            cls = EightBallGame

        return cls

    @staticmethod
    def _create_records(players):
        records = []
        for player in players:
            name = player.pop('name')
            player_key = User.query(User.name == name).get(keys_only=True)
            player['player_key'] = player_key
            record = PoolPlayerRecord(**player)
            records.append(record)
        ndb.put_multi(records)
        return records

    @staticmethod
    def _is_valid_data(data):
        game_type = data.get('game_type')
        players = data.get('players')

        if not all([game_type, players]):
            return False

        if not isinstance(game_type, basestring):
            return False

        if not isinstance(players, list):
            return False

        return True


def setup_urls(app):
    app.add_url_rule(
        '/api/game/',
        view_func=GameAPI.as_view('api.game'))
