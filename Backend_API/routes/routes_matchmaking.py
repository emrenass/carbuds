from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *
from Backend_API.init_app import app
import json
import time
import urllib
import urllib3



route_matchmaking = Blueprint('route_matchmaking', __name__)


@route_matchmaking.route('/set_trip_driver', methods=['POST'])
def set_trip_driver():
    direction_api_key = app.config["DIRECTIONS_API_KEY"]
    directions_base_url = 'http://maps.googleapis.com/maps/api/directions/json'
    url = directions_base_url + '?' + urllib.urlencode({
        'origin': "%s,%s" % ("38.453", "45.7654"),
        'destination': "%s,%s" % ("38.543", "45.7642"),
        'key': direction_api_key,
    })

    response = str(urllib3.urlopen(url).read())
    result = json.loads(response.replace('\\n', ''))

    user_id = 1
    start_lat, start_lon = tuple(request.form['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.form['trip_start_point'].split(','))
    trip_start_time = request.form['trip_start_time']
    available_seat = request.form['available_seat']

    query = """INSERT INTO driver_matchmaking_pool 
                    (user_id, trip_start_point, trip_end_point, available_seat, trip_start_time)
                    VALUES ('%s', point('%f', '%f'), point('%f', '%f'), '%s', '%s')""" \
            % (user_id, float(start_lat), float(start_lon),
               float(end_lat), float(end_lon), available_seat, trip_start_time)

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)


@route_matchmaking.route('/set_trip_hitchhiker', methods=['POST'])
def set_trip_hitchhiker():
    user_id = 1
    start_lat, start_lon = tuple(request.form['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.form['trip_start_point'].split(','))
    trip_start_time = request.form['trip_start_time']

    query = """INSERT INTO hitchhiker_matchmaking_pool 
                        (user_id, trip_start_point, trip_end_point, trip_start_time)
                        VALUES ('%s', point('%f', '%f'), point('%f', '%f'), '%s')""" \
            % (user_id, float(start_lat), float(start_lon),
               float(end_lat), float(end_lon), trip_start_time)

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)

@route_matchmaking.route('/get_destination', methods=['POST'])
def get_destination():
    user_id = 1
