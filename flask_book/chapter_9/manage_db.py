from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import *
import datetime
import datetime
from sqlalchemy import asc, desc
from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore


db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DevelopmentConfig.SQLALCHEMY_DATABASE_URI

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


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


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


user_datastore = SQLAlchemyUserDatastore(db, User, Role)



class Tracking(db.Model):
    __tablename__ = "tracking"
    id = db.Column(db.Integer, primary_key=True)
    user_ip = db.Column(db.String(46))
    user_agent = db.Column(db.String(100))
    at_time = db.Column(db.DateTime, default=datetime.datetime.now)

if __name__ == '__main__':
    manager.run()