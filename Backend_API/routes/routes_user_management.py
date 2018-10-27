from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *

route_user_management = Blueprint('route_user_management', __name__)


@route_user_management.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    query = """SELECT * FROM "User" WHERE "username" = '%s' AND "password" = '%s'""" % (username, password)

    conn = db_connection()
    result = execute_query(query, conn)

    if result:
        return jsonify(True)
    else:
        return jsonify(False)


@route_user_management.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    pass


@route_user_management.route('/signup', methods=['GET', 'POST'])
def signup():
    name = request.form['name']
    surname = request.form['surname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    query = """INSERT INTO "User" (name, lastname, username, password, email)
                VALUES ('%s', '%s', '%s', '%s', '%s')""" % (name, surname, username, password, email)

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)


# Should be used each time a user logs in to check whether the user freshly signed up or not
@route_user_management.route('/is_new_user', methods=['GET', 'POST'])
@login_required
def is_new_user():
    pass


@route_user_management.route('/initial_role_selection', methods=['GET', 'POST'])
@login_required
def initial_role_selection():
    pass


@route_user_management.route('/initial_driver_profile_setup', methods=['POST'])
@login_required
def initial_driver_profile_setup():
    gender_pref = request.form['gender_preference']
    musid_pref = request.form['music_preference']
    passanger_seats = request.form['passanger_seats']
    # TODO: Check licence plate validity
    car_licence_plate = request.form['licence_plate']
    car_model = request.form['car_model']
    user_id = 1
    musid_pref = '{%s}'
    query = """INSERT INTO "driver_profile" (user_id, car_model, hitchhiker_gender_preference, music_prefrence)
                VALUES (%s, %s, '%s', '{"Pop", "Rock"}') """ % (1, car_model, gender_pref)

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)


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
