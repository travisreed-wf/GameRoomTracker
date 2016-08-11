from flask import Flask

from src.api import game as game_api
from src.api import user as user_api
from src.home import views as home_views
from src.stats import views as stats_views


app = Flask(__name__)
app.debug = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "SecretKey"

game_api.setup_urls(app)
home_views.setup_urls(app)
stats_views.setup_urls(app)
user_api.setup_urls(app)
