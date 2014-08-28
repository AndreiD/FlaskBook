import logging
from flask import render_template, request, flash
from models import *
from forms import *
from flask.ext.security import Security, login_required, logout_user
from app import *


security = Security(app, user_datastore)

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    new_tracking = Tracking()
    new_tracking.add_data(request.remote_addr, request.headers.get('User-Agent'))

    list_records = new_tracking.list_all_users(page, app.config['LISTINGS_PER_PAGE'])

    return render_template("index.html", list_records=list_records)


@app.route('/track', methods=['GET', 'POST'])
@app.route('/track/<user_ip>', methods=['GET', 'POST'])
@app.route('/track/<user_ip>/<int:page>', methods=['GET', 'POST'])
def track_user_ip(user_ip="", page=1):

    form = QueryOneForm(request.form)

    if request.method == 'POST':
        if form.validate():
            user_ip = form.user_ip.data


    new_tracking = Tracking()
    list_records = new_tracking.track_user_ip(user_ip, page, app.config['LISTINGS_PER_PAGE'])

    return render_template("track_ip.html", list_records=list_records, form=form, user_ip = user_ip)


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form = TrackingInfoForm(request.form)

    if request.method == 'POST':
        if form.validate():
            new_tracking = Tracking()

            user_ip = form.user_ip.data
            user_agent = form.user_agent.data

            logging.info("adding " + user_ip + " " + user_agent)

            new_tracking.add_data(user_ip, user_agent)

            flash("added successfully", category="success")



    return render_template("add_record.html", form=form)


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')