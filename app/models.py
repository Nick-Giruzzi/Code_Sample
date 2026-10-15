#!/usr/bin/python3

from flask_login import UserMixin, AnonymousUserMixin

# Local import
from app.extensions import db

class Anonymous(AnonymousUserMixin):
    id = 0
    first_name = 'Guest'
    username = 'Guest'
    email = ''
    password = ''
    role = None    


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    created = db.Column(db.DateTime, nullable=False)
    mfa = db.Column(db.Boolean,nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "fn": self.first_name,
            "ln": self.last_name,
            "un": self.username,
            "email": self.email,
            #"created": self.created.strftime("")
            "mfa": self.mfa
        }


class Logins(db.Model):
    __tablename__ = 'Logins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    originated = db.Column(db.String)
    date = db.Column(db.DateTime, nullable=False)
    session_type = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "originated": self.originated
        }


class MFACodes(db.Model):
    __tablename__ = 'MFACodes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), unique=True)
    mfa_code = db.Column(db.String, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)


class Accounts(db.Model):
    __tablename__ = 'Accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    acc_type = db.Column(db.String, nullable=False)
    number = db.Column(db.String, unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)


class Transactions(db.Model):
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    acc_id = db.Column(db.Integer, db.ForeignKey("Accounts.id"))
    trans_type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)