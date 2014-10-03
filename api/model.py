"""
Author: Tomas
Date : 2014-03-02
Desc: QASystem's Database model, Use Flask-mongoengine
"""
from api import db
from flask.ext.login import UserMixin
from bson.objectid import ObjectId
from flask.ext.mongoengine import ValidationError
import uuid

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
    sign_pwd = db.StringField(required=True)
    name = db.StringField(required=True, unique=True)
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

    def user(self):
        return self

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({'id': self.id})

    def get_id(self):
        return unicode(self.id)


class Client(db.Document):
    client_id = db.StringField(unique=True)
    client_secret = db.StringField(unique=True)
    is_credital = db.BooleanField(default = True)
    user = db.ReferenceField(User, dbref = True)
    _redirect_uris = db.ListField(db.StringField())
    _default_scopes = db.StringField()

    @property
    def client_type(self):
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris
        return list()

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes
        return list()

class Grant(db.Document):
    user_id = db.ReferenceField(User, dbref = True)
    client = db.ReferenceField(Client, dbref = True)
    code = db.StringField()
    redirect_uri = db.StringField()
    expires = db.DateTimeField()
    _scopes = db.ListField(db.StringField())

    def delete(self):
        pass

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes
        return list()

class Token(db.Document):
    client = db.ReferenceField(Client, dbref = True)
    user = db.ReferenceField(User, dbref = True)
    token_type = db.StringField(unique = True)
    access_token = db.StringField(unique = True)
    refresh_token = db.StringField(unique = True)
    expires = db.DateTimeField()
    _scopes = db.ListField(db.StringField())

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes
        return list()

"""
class GlobalSession(db.Document):
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
"""
