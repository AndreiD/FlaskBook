import logging
from flask import render_template, request, flash, redirect
from models import *
from forms import *
from flask.ext.security import Security, login_required, logout_user, roles_required, current_user, utils
from app import *
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView



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
@roles_required('admin')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/logout')
def log_out():
    logout_user()
    return redirect(request.args.get('next') or '/')




# Executes before the first request is processed.
@app.before_first_request
def before_first_request():

    logging.info("-------------------- initializing everything ---------------------")
    db.create_all()

    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='end-user', description='End user')

    encrypted_password = utils.encrypt_password('123123')
    if not user_datastore.get_user('me@me.com'):
        user_datastore.create_user(email='me@me.com', password=encrypted_password, active=True, confirmed_at=datetime.datetime.now())

    encrypted_password = utils.encrypt_password('123123')
    if not user_datastore.get_user('enduser@enduser.com'):
        user_datastore.create_user(email='enduser@enduser.com', password=encrypted_password, active=True, confirmed_at=datetime.datetime.now())

    db.session.commit()

    user_datastore.add_role_to_user('me@me.com', 'admin')
    user_datastore.add_role_to_user('enduser@enduser.com', 'end-user')
    db.session.commit()


# -------------------------- ADMIN PART ------------------------------------
admin = Admin(app, name="Flask Test Admin")


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class TrackingAdminView(ModelView):

    can_create = True

    def is_accessible(self):
        # write your protection here!!!
        return True


    def __init__(self, session, **kwargs):
        super(TrackingAdminView, self).__init__(Tracking, session, **kwargs)


class UserAdminView(ModelView):
    column_exclude_list = ('password')
    def is_accessible(self):
        return current_user.has_role('admin')


    def __init__(self, session, **kwargs):
        super(UserAdminView, self).__init__(User, session, **kwargs)

class RoleView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')
    def __init__(self, session, **kwargs):
        super(RoleView, self).__init__(Role, session, **kwargs)


admin.add_view(TrackingAdminView(db.session))
admin.add_view(UserAdminView(db.session))
admin.add_view(RoleView(db.session))

# -------------------------- ADMIN PART END ---------------------------------