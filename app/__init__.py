from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create instance of app variable
app = Flask(__name__)

# all other variable instances coming after the app instance
bootstrap = Bootstrap(app)
app.config.from_object(Config)

# app variables for database usage
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app variables for Login
login = LoginManager(app)
# login route
login.logi_view = 'login'

# routes to load home page
from app import routes
