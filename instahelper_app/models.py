from flask_login import UserMixin
from instahelper_app import login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    acc_limit = db.Column(db.Integer, nullable=False, default=1)
    accounts = db.relationship('Account', backref='accountinfo', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.accounts})"

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hashtag_commands = db.relationship('Hashtag', backref='hashtag', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.owner})"

class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    tags = db.Column(db.String)
    posts = db.Column(db.String)
    liked = db.Column(db.String)
    commented = db.Column(db.String)
    like = db.Column(db.Boolean)
    comment = db.Column(db.Boolean)
    follow = db.Column(db.Boolean)

    def __repr__(self):
        return f"User({self.id})"

