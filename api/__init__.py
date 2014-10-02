from flask import Flask
from flask.ext.restful import Api
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager
from flask.ext.login import LoginManager

app = Flask(__name__)
api = Api(app)
manager = Manager(app)

app.config.from_object('develop_conf')

db = MongoEngine(app)

from api.users import UserAPI
from api.login import LoginAPI

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return 'unauthorized'

@login_manager.user_loader
def load_user(userid):
    return model.User.objects.with_id(userid)

import model
