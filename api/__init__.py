from flask import Flask, request
from flask.ext.restful import Api
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager
from flask.ext.login import LoginManager
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__)
api = Api(app)
manager = Manager(app)

app.config.from_object('develop_conf')

db = MongoEngine(app)

oauth = OAuth2Provider(app)

#route
from api.users import UserAPI
from api.login import LoginAPI
from api.oauthServer import AuthorizeAPI, TokenAPI, MeAPI

login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    return 'unauthorized'

@login_manager.user_loader
def load_user(userid):
    return model.User.objects.with_id(userid)

@oauth.clientgetter
def load_client(client_id):
    return model.Client.objects(client_id = client_id).first()

@oauth.grantgetter
def load_grant(client_id, code):
    return model.Grant.objects(client_id=client_id, code=code).first()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id = client_id,
        code = code['code'],
        redirect_uri = request.redirect_uri,
        _scopes = list(*request.scopes),
        user = current_user.user(),
    ).save()
    return grant

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return model.Token.objects(access_token=access_token).first()
    return model.Token.objects(refresh_token=refresh_token).first()

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = model.Token.objects(client_id = request.client.client_id,
            user_id = request.user.id)

    for t in toks:
        session.delete(t)

    tok = Token(access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    ).save()
    return tok


import model
