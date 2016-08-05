from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from src.home import views as home_views


app = Flask(__name__)
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.secret_key = "SecretKey"

toolbar = DebugToolbarExtension(app)

home_views.setup_urls(app)
