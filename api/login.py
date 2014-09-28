#-*- coding:utf-8 -*-
from flask import request
from api import api
from model import User
from flask.ext.restful import Resource, reqparse
#Login.py
class LoginAPI(Resource):
    def __init__(self):
        pass
    def put(self):
        return request.get_json(force=True)
    def delete(self):
        return request.get_json(force=True)

api.add_resource(LoginAPI, '/loginout/', endpoint='loginout')
