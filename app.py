#-*- coding:utf-8 -*-
from flask import Flask, request
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api, Resource, reqparse
from flask.ext.login import UserMixin
from bson.objectid import ObjectId
from flask.ext.mongoengine import ValidationError

#api/__init__.py
app = Flask(__name__)
api = Api(app)

app.config.from_object('develop_conf')

db = MongoEngine(app)

class User(db.Document, UserMixin):
    """
    It's for user system schema, it is store in the collection named users.

    account : account Field
    pwd : Password Field
    name : Nickname Field
    email : Email Field
    get_id : return the unicode of uid
    get_user : return a user object
    """
    account = db.StringField( required=True, unique=True)
    pwd = db.StringField(required=True)
    name = db.StringField()
    email = db.EmailField(unique=True)
    group = db.StringField()
    logo = db.StringField()
    lastlogin = db.DateTimeField()
    IP = db.StringField()
    Quota = db.FloatField()
    old_logo = db.ListField(db.StringField())
    skills = db.StringField()
    demourl = db.ListField(db.StringField())

    meta = {
            'collection': 'users'
    }

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(token)
        user = User.objects.with_id(data['id'])
        return user

    def get_id(self):
        return unicode(self.id)

    def EditUser(self, newinfo):
        try:
            status = self.objects.exclude('users').update(**newinfo)
        except ValidationError as e:
            return e.to_dict()
        return status

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

#Login.py
class LoginAPI(Resource):
    def __init__(self):
        pass
    def put(self):
        return request.get_json(force=True)
    def delete(self):
        return request.get_json(force=True)

api.add_resource(UserAPI, '/users/', endpoint='user')
api.add_resource(UserAPI, '/loginout/', endpoint='loginout')

if __name__ == '__main__':
    app.run()
