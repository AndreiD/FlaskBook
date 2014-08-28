import datetime
from app import db


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

    def list_all_users(self):
        return Tracking.query.all()


    def __repr__(self):
        return '<Tracking %r>' % (self.id)