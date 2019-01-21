from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pkgutil import iter_modules
from flask_cors import CORS

app = Flask(__name__)

app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
CORS(app, supports_credentials=True)
from . import Model
from .Controller import *

