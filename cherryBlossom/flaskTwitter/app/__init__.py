from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import views, models

from .models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view =  "index"

@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id==userid).first()


