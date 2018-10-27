from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from utils.decorators import login_required

route_user_management = Blueprint('route_user_management', __name__)


@route_user_management.route('/login', methods=['GET', 'POST'])
def login():
    pass


@route_user_management.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    pass


@route_user_management.route('/signup', methods=['GET', 'POST'])
def signup():
    pass


# Should be used each time a user logs in to check whether the user freshly signed up or not
@route_user_management.route('/is_new_user', methods=['GET', 'POST'])
@login_required
def is_new_user():
    pass


@route_user_management.route('/initial_role_selection', methods=['GET', 'POST'])
@login_required
def initial_role_selection():
    pass


@route_user_management.route('/initial_driver_profile_setup', methods=['GET', 'POST'])
@login_required
def initial_driver_profile_setup():
    pass


@route_user_management.route('/initial_hitchhiker_profile_setup', methods=['GET', 'POST'])
@login_required
def initial_hitchhiker_profile_setup():
    pass


@route_user_management.route('/update_driver_profile', methods=['GET', 'POST'])
@login_required
def update_driver_profile():
    pass


@route_user_management.route('/update_hitchhiker_profile', methods=['GET', 'POST'])
@login_required
def update_hitchhiker_profile():
    pass
