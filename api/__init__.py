from flask import Flask
from flask.ext.restful import Api
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager

app = Flask(__name__)
api = Api(app)
manager = Manager(app)

app.config.from_object('develop_conf')

db = MongoEngine(app)

from api.users import UserAPI
from api.login import LoginAPI

import model
