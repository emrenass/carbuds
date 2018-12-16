from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *
import jwt

route_user_management = Blueprint('route_user_management', __name__)


@route_user_management.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']

    query = """SELECT * FROM Users WHERE "username" = '%s' AND "password" = '%s'""" % (username, password)

    conn = db_connection()
    result = execute_query(query, conn)

    if result:
        message = {
                  "username": username,
                  "user_id": result[0]["id"]
            }
        return jwt.encode(message, app.config['SECRET_KEY'], algorithm='HS256')
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
    gender = request.json['gender']
    device_reg_id = request.json['device_reg_id']

    query = """INSERT INTO Users (name, lastname, username, password, email, gender, device_reg_id)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                % (name, surname, username, password, email, gender, device_reg_id)

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
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    gender_pref = request.json['gender_preference']
    music_pref = request.json['music_preference']
    passenger_seats = request.json['passenger_seats']
    # TODO: Check licence plate validity
    car_license_plate = request.json['license_plate']
    brand = request.json['car_brand']
    model = request.json['car_model']
    user_id = token['user_id']

    query_brand = """SELECT cm.id 
                      FROM car_brand cb 
                      INNER JOIN car_model cm ON cb.id = cm.brand_id 
                      WHERE cm.model='%s' AND cb.brand = '%s'""" % (
        model, brand)

    conn = db_connection()
    try:
        result = execute_query(query_brand, conn)
        model_id = result[0]["id"]
    except Exception as e:
        print(e)
        return jsonify(e)
    query = """INSERT INTO "driver_profile" (user_id, car_model, hitchhiker_gender_preference, music_preference, passenger_seat, license_plate)
                VALUES (%s, %s, '%s', '%s', %s, '%s') """ % (
        user_id, model_id, gender_pref, music_pref, passenger_seats, car_license_plate)
    query_update = """UPDATE users 
                        SET current_profile='Driver' 
                        WHERE id=%s""" % user_id

    conn = db_connection()

    try:
        commit_query_multiple([query, query_update], conn)
        # commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)


@route_user_management.route('/initial_hitchhiker_profile_setup', methods=['GET', 'POST'])
@login_required
def initial_hitchhiker_profile_setup():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
    gender_pref = request.json['gender_preference']
    music_pref = request.json['music_preference']
    # TODO: Check licence plate validity
    query = """INSERT INTO "hitchhiker_profile" (user_id, driver_gender_preference, music_preference)
                    VALUES (%s, '%s', '%s') """ % (user_id, gender_pref, music_pref)
    query_update = """UPDATE users SET current_profile='Hitchhiker' WHERE id=%s""" % user_id

    conn = db_connection()

    try:
        # commit_query(query, conn)
        commit_query_multiple([query, query_update], conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)
    pass


@route_user_management.route('/update_driver_profile', methods=['POST'])
@login_required
def update_driver_profile():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
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
        return jsonify(str(e))

    query = """UPDATE driver_profile SET car_model = %s, license_plate = '%s', hitchhiker_gender_preference = '%s', 
                music_preference = '%s', passenger_seat = %s WHERE user_id = %s""" % (
        model_id, json["license_plate"], json["hitchhiker_gender_preference"],
        json["music_preference"], json["passenger_seats"], user_id)

    conn = db_connection()
    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)


@route_user_management.route('/update_hitchhiker_profile', methods=['GET', 'POST'])
@login_required
def update_hitchhiker_profile():
    json = request.json
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
    query = """UPDATE hitchhiker_profile SET driver_gender_preference = '%s', 
                    music_preference = '%s'WHERE user_id = %s""" % (
        json["gender_preference"], json["music_preference"], user_id)

    conn = db_connection()
    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)



@route_user_management.route('/switch_profile', methods=['GET', 'POST'])
@login_required
def switch_profile():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
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
