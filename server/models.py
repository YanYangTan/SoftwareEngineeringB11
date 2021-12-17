from . import db


class User(db.Model):
    __tablename__ = 'users'
    idusers = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(45), unique=True)
    phone = db.Column(db.String(45))
    birthday = db.Column(db.Date)
    quote = db.Column(db.Text)

    relation_group_user = db.relationship("RelationGroupUser", backref="users")


class Group(db.Model):
    __tablename__ = 'groups'
    idgroups = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    invite_key = db.Column(db.String(45))
    key_expiry_date = db.Column(db.DateTime)

    relation_group_user = db.relationship("RelationGroupUser", backref="groups")


class RelationGroupUser(db.Model):
    __tablename__ = 'relation_group_user'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.idgroups'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
    admin = db.Column(db.Boolean, default=False)


class Gathering(db.Model):
    __tablename__ = 'gathering'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.idgroups'))
    name = db.Column(db.String(45))
    description = db.Column(db.Text)
    enddate = db.Column(db.DateTime)
    status = db.Column(db.Boolean, default=False)
    allow_multiple_vote = db.Column(db.Boolean, default=False)

    relation_gathering = db.relationship("RelationGathering", backref="gathering")


class Suggestion(db.Model):
    __tablename__ = 'suggestion'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
    content = db.Column(db.Text)

    relation_gathering = db.relationship("RelationGathering", backref="suggestion")


class VoteOptions(db.Model):
    __tablename__ = 'vote_options'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    vote_count = db.Column(db.Integer, default=0)
    voters = db.Column(db.Text)

    relation_gathering = db.relationship("RelationGathering", backref="vote_options")


class RelationGathering(db.Model):
    __tablename__ = 'relation_gathering'
    id = db.Column(db.Integer, primary_key=True)
    gathering_id = db.Column(db.Integer, db.ForeignKey('gathering.id'))
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestion.id'))
    vote_id = db.Column(db.Integer, db.ForeignKey('vote_options.id'))
    status = db.Column(db.Boolean)


class Calendar(db.Model):
    __tablename__ = 'calendar'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.idgroups'))
    content = db.Column(db.Text)


class UserCalendar(db.Model):
    __tablename__ = 'calendar_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
    content = db.Column(db.Text)


class PhotoPost(db.Model):
    __tablename__ = 'photo_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
    group_id = db.Column(db.Integer, db.ForeignKey('groups.idgroups'))
    caption = db.Column(db.Text)
    media = db.Column(db.Text)
    like = db.Column(db.Integer)
    like_users = db.Column(db.Text)
    date_created = db.Column(db.DateTime)

    relation_post_comment = db.relationship("RelationPostComment", backref="photo_post")


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.idusers'))
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime)

    relation_post_comment = db.relationship("RelationPostComment", backref="comments")


class RelationPostComment(db.Model):
    __tablename__ = 'relation_post_comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('photo_post.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))


class Genealogy(db.Model):
    __tablename__ = 'genealogy'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.idgroups'))
    content = db.Column(db.Text)
