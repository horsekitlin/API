from flask import request, jsonify
from flask.ext.login import login_required, current_user
from model import Client
from api import api, oauth
from werkzeug.security import gen_salt
from flask.ext.restful import Resource, reqparse

class TokenAPI(Resource):
    @oauth.token_handler
    def get(self):
        return None

class AuthorizeAPI(Resource):
    @oauth.authorize_handler
    def get(self, *args, **kwargs):
        user = current_user.user()
        client_id = kwargs.get('client_id')
        client = Client.objects(client_id = client_id).first()
        return {"user":user, "client":client}

class MeAPI(Resource):
    @oauth.require_oauth()
    def get(self):
        user = request.oauth.user
        return jsonify(username = user.username)

class ClientAPI(Resource):
    def post(self):
        user = current_user.user()
        item = Client(
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=list([
                'http://localhost:8000/authorized',
                'http://127.0.0.1:8000/authorized',
                'http://127.0.1:8000/authorized',
                'http://127.1:8000/authorized',
                ]),
            _default_scopes='email',
            user=user,
        )
        try:
            item.save()
        except:
            return 'insert false'
        return jsonify(
                client_id = item.client_id,
                client_secret = item.client_secret
                )


api.add_resource(TokenAPI, '/oauth/token', endpoint='token')
api.add_resource(AuthorizeAPI, '/oauth/authorize', endpoint='authorize')
api.add_resource(MeAPI, '/oauth/me', endpoint='me')
api.add_resource(ClientAPI, '/client', endpoint='client')

