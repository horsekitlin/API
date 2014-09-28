"""
Author: Tomas
Date : 2014-03-02
Desc: QASystem's Database model, Use Flask-mongoengine
"""
from app import db
from flask.ext.login import UserMixin
from bson.objectid import ObjectId
from flask.ext.mongoengine import ValidationError

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
    account = db.StringField( required=True)
    pwd = db.StringField(required=True)
    name = db.StringField()
    email = db.EmailField()
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

class GlobalSession(db.Document):
    """
        Global Session store
    """
    uid = db.ObjectIdField()

    meta = {
        "collection" : "GlobalSession"
    }

    def CheckUser(self):
        UCount = User.objects(id = self.uid).count()
        if UCount < 1:
            raise ValidationError(message = u'User Not exist')
        elif UCount > 1:
            raise ValidationError(message = u'User already Login')
        else:
            GlobalSession.objects(uid = self.uid).delete()
            sid = self.save()
            return  sid
        return False

    def Logout(self):
        GlobalSession.objects(id = ObjectId(self.id)).delete()
        return True
