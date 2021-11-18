from . import db


class User(db.Model):
    __tablename__ = 'users'
    idusers = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(45), unique=True)
    phone = db.Column(db.String(45))
    birthday = db.Column(db.Date)

    relation_group_user = db.relationship("RelationGroupUser", backref="users")


class Group(db.Model):
    __tablename__ = 'groups'
    idgroups = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    invite_key = db.Column(db.String(45))

    relation_group_user = db.relationship("RelationGroupUser", backref="groups")


class RelationGroupUser(db.Model):
    __tablename__ = 'relation_group_user'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.idgroups'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
