from flask import Flask

# first create app object as an instance of flask class
app = Flask(__name__) 

from app import routes
from app import cli
