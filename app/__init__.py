import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from flask_login import LoginManager

my_metadata = MetaData()

class Base(DeclarativeBase):
  metadata = my_metadata
  
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)
  login.init_app(app)
  login.login_view = 'login'

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp)

  from app.cli import bp as cli_bp
  app.register_blueprint(cli_bp)

  
  return app

from app import models