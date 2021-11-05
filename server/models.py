from . import db


class User(db.Model):
    __tablename__ = 'users'
    idusers = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(45), unique=True)
    phone = db.Column(db.String(45))
    birthday = db.Column(db.Date)