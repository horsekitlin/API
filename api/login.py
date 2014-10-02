#-*- coding:utf-8 -*-
from flask import request
from api import api
from itsdangerous import Signer
from model import User
from flask.ext.restful import Resource, reqparse
from flask.ext.login import (login_user, logout_user,
        current_user, login_required)

class LoginAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('account', type=str, help=u'No account exist')

    def put(self):
        data = request.get_json(force=True)
        data['sign_pwd'] = Signer(data['pwd']).sign('pwd')
        try:
            user = User.objects(**data).first()
        except:
            return 'Search DB Error'
        if user:
            login_user(user)
            return user.to_json()
        return  'Account or PasswordError'

    @login_required
    def delete(self):
        logout_user()
        return 'Logout Success!'

api.add_resource(LoginAPI, '/loginout/', endpoint='loginout')
