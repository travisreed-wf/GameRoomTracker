from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from src.game import api as game_api
from src.home import views as home_views
from src.user import api as user_api


app = Flask(__name__)
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "SecretKey"

toolbar = DebugToolbarExtension(app)

game_api.setup_urls(app)
home_views.setup_urls(app)
user_api.setup_urls(app)
