from flask import Flask
from config import Config

# first create app object as an instance of flask class
app = Flask(__name__) 
app.config.from_object(Config)

from app import routes
from app import cli
