import datetime
from app import db
from sqlalchemy import asc, desc
from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore



roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))




class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    def __repr__(self):
        return '<models.User[email=%s]>' % self.email

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

class Tracking(db.Model):
    __tablename__ = "tracking"
    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String(46))
    user_agent = db.Column(db.String(100))
    at_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def add_data(self, user_ip, user_agent):
        new_user = Tracking(user_ip=user_ip, user_agent=user_agent)
        db.session.add(new_user)
        db.session.commit()

    def list_all_users(self,page, LISTINGS_PER_PAGE):
        return Tracking.query.order_by(desc(Tracking.at_time)).paginate(page, LISTINGS_PER_PAGE, False)

    def track_user_ip(self, user_ip, page, LISTINGS_PER_PAGE):
        return Tracking.query.filter(Tracking.user_ip == user_ip).order_by(desc(Tracking.at_time)).paginate(page, LISTINGS_PER_PAGE, False)


    def __repr__(self):
        return '<Tracking %r>' % (self.id)