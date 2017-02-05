# -*- encoding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_autodoc import Autodoc

from WarehouseServer import serial_thread

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'uj3eXpQTRqWm3Acg5W9i243f46bwn4BN'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["JSON_SORT_KEYS"] = False

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
com = serial_thread.WarehouseCommunicator()
auto = Autodoc(app)

from WarehouseServer import views, models
from models import User

