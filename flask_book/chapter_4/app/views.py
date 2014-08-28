from flask import render_template, request
from models import *
from app import *

# Executes before the first request is processed.
@app.before_first_request
def before_first_request():
    logging.info("-------------------- initializing everything ---------------------")
    db.create_all()

@app.route('/')
@app.route('/index')
def index():

    new_tracking = Tracking()
    new_tracking.add_data(request.remote_addr,request.headers.get('User-Agent'))

    list_records = new_tracking.list_all_users()

    for record in list_records:
        logging.info(record.user_ip + " " + record.user_agent)

    return render_template("index.html")



