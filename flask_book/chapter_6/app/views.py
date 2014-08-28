from flask import render_template, request
from app import *
from models import *
import logging



@app.before_first_request
def before_first_request():
    logging.info("-------------------- initializing everything ---------------------")
    db.create_all()


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    new_tracking = Tracking()
    new_tracking.add_data(request.remote_addr, request.headers.get('User-Agent'))

    list_records = new_tracking.list_all_users(page, app.config['LISTINGS_PER_PAGE'])

    return render_template("index.html", list_records=list_records)


@app.route('/track/<user_ip>')
@app.route('/track/<user_ip>/<int:page>')
def track_user_ip(user_ip="", page = 1):

    new_tracking = Tracking()
    list_records = new_tracking.track_user_ip(user_ip, page, app.config['LISTINGS_PER_PAGE'])

    return render_template("track_ip.html", list_records=list_records)


