# -*- coding: utf-8 -*-

from app import *
from wtforms.validators import Required, Length, IPAddress
from wtforms import Form, TextField


class TrackingInfoForm(Form):
    user_ip = TextField('user_ip', validators=[Required(), IPAddress(message="Invalid IP Address")])
    user_agent = TextField('user_agent', validators=[Length(max=46, message='max 46 characters')])


class QueryOneForm(Form):
    user_ip = TextField('user_ip', validators=[Required(), IPAddress(message="Invalid IP Address")])


