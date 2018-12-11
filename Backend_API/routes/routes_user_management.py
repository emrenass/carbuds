from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *

route_user_management = Blueprint('route_user_management', __name__)


@route_user_management.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    query = """SELECT * FROM Users WHERE "username" = '%s' AND "password" = '%s'""" % (username, password)

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
    name = request.json['name']
    surname = request.json['surname']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    query = """INSERT INTO Users (name, lastname, username, password, email)
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
    gender_pref = request.json['gender_preference']
    music_pref = request.json['music_preference']
    passanger_seats = request.json['passanger_seats']
    # TODO: Check licence plate validity
    car_licence_plate = request.json['licence_plate']
    brand = request.json['car_brand']
    model = request.json['car_model']
    user_id = request.json['user_id']

    query_brand = """SELECT cm.id FROM car_brand cb INNER JOIN car_model cm ON cb.id = cm.brand_id WHERE cm.model='%s' AND cb.brand = '%s'""" % (
        model, brand)

    conn = db_connection()
    try:
        result = execute_query(query_brand, conn)
        model_id = result[0]["id"]
    except Exception as e:
        print(e)
        return jsonify(e)
    query = """INSERT INTO "driver_profile" (user_id, car_model, hitchhiker_gender_preference, music_prefrence, passenger_seat)
                VALUES (%s, %s, '%s', '%s', %s) """ % (user_id, model_id, gender_pref, music_pref, passanger_seats)
    query_update = """UPDATE users SET current_profile='Driver'"""

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
    user_id = request.json['user_id']
    gender_pref = request.json['gender_preference']
    music_pref = request.json['music_preference']
    # TODO: Check licence plate validity
    query = """INSERT INTO "driver_profile" (user_id, hitchhiker_gender_preference, music_prefrence)
                    VALUES (%s, '%s', '%s') """ % (user_id, gender_pref, music_pref)
    query_update = """UPDATE users SET current_profile='Hitchhiker'"""

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)
    pass


@route_user_management.route('/update_driver_profile', methods=['POST'])
@login_required
def update_driver_profile():
    json = request.json
    model = json["car_model"]
    brand = json["car_brand"]

    query_brand = """SELECT cm.id FROM car_brand cb INNER JOIN car_model cm ON cb.id = cm.brand_id WHERE cm.model='%s' AND cb.brand = '%s'""" % (
    model, brand)

    conn = db_connection()
    try:
        result = execute_query(query_brand, conn)
        model_id = result[0]["id"]
    except Exception as e:
        print(e)
        return jsonify(e)

    query = """UPDATE driver_profile SET car_model = %s, license_plate = '%s', hitchhiker_gender_preference = '%s', 
                music_prefrence = '%s', passenger_seat = %s WHERE user_id = %s""" % (
                                                model_id, json["license_plate"], json["hitchhiker_gender_preference"],
                                                json["music_prefrence"], json["passenger_seat"], json["user_id"])

    conn = db_connection()
    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)


@route_user_management.route('/update_hitchhiker_profile', methods=['GET', 'POST'])
def update_hitchhiker_profile():
    json = request.json

    query = """UPDATE hitchhiker_profile SET driver_gender_preference = '%s', 
                    music_prefrence = '%s'WHERE user_id = %s""" % (
        json["driver_gender_preference"], json["music_prefrence"], json["user_id"])

    conn = db_connection()
    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)
    pass


@route_user_management.route('/switch_profile', methods=['GET', 'POST'])
@login_required
def switch_profile():
    user_id = 1
    switch_to = ""
    conn = db_connection()
    query = """SELECT current_profile FROM users WHERE id = %s""" % (user_id)
    try:
        row = execute_query(query, conn)
        if row[0]["current_profile"] == "Driver":
            switch_to = "Hitchhiker"
        else:
            switch_to = "Driver"

        conn = db_connection()
        query = """UPDATE users SET current_profile='%s' WHERE id=%s""" % (switch_to, user_id)
        commit_query(query, conn)

        return jsonify(True)
    except Exception as e:
        print(e)
        return jsonify(e)

