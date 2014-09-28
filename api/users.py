#-*- coding:utf-8 -*-
from flask import request
from api import api
from model import User
from flask.ext.restful import Resource, reqparse
from flask.ext.mongoengine import ValidationError

#User.py
class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('account', type=str, help = u'No account exist!', location = 'json')
        self.reqparse.add_argument('email', type=str, help = u'No email exist!', location = 'json')
        self.reqparse.add_argument('pwd', type=str, help = u'No pwd exist!', location = 'json')
        self.reqparse.add_argument('skills', type=str, help = u'No skills exist!', location = 'json')
    def post(self):
        data = request.get_json(force=True)
        try:
            users = User.objects(**data)
        except:
            raise ValidationError(message = u'搜尋資料庫失敗')
        return users.to_json(), 201

    def put(self):
        data = request.get_json(force=True)
        try:
            Obj = User(**data).save()
        except:
            raise ValidationError(message = u'資料錯誤，寫入資料庫失敗')

        return Obj.to_json(), 201

    def update(self):
        """
        {
        "new":{
            "set__name": "Tomas1111111"
        },
        "old":{
            "skills": "skill",
            "email": "horsekit1982@gmail.com",
            "account": "tomas111",
            "pwd": "123456",
            "name": "Tomas"
            }
        }
        """
        data = request.get_json(force=True)
        try:
            User.objects(**data['old']).update(**data['new'])
        except:
            raise ValidationError(message = u'資料錯誤，修改資料庫失敗')
        return 'success',201

    def delete(self):
        return request.get_json(force=True)


api.add_resource(UserAPI, '/users/', endpoint='user')
