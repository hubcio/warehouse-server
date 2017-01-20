# -*- encoding: utf-8 -*-

from WarehouseServer import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    role = db.Column(db.String(32))
    date = db.Column(db.DateTime)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def add_super_admin():
        username = 'admin'
        if User.query.filter_by(username=username).first() is not None:
            print ("Admin exists!")
            return
        password = '13371337'
        role = 'admin'
        user = User(username=username, role=role)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()


class Cell(db.Model):
    __tablename__ = 'cells'
    id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(128), index=True)
    accessible_by = db.Column(db.Integer)
    rfid = db.Column(db.String(128), unique=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    z = db.Column(db.Integer)
