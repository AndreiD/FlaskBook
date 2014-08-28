from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import logging


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from app import views, models, forms
