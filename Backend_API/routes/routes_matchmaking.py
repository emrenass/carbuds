from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *
import urllib.parse
import requests
import polyline


route_matchmaking = Blueprint('route_matchmaking', __name__)


@route_matchmaking.route('/set_trip_driver', methods=['POST'])
def set_trip_driver():
    user_id = 1
    start_lat, start_lon = tuple(request.json['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.json['trip_end_point'].split(','))
    trip_start_time = request.json['trip_start_time']
    available_seat = request.json['available_seat']
    direction_api_key = app.config["DIRECTIONS_API_KEY"]
    directions_base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    url = directions_base_url + '?' + urllib.parse.urlencode({
        'origin': "%s,%s" % (start_lat, start_lon),
        'destination': "%s,%s" % (end_lat, end_lon),
        'key': direction_api_key,
    })

    response = requests.get(url)
    result = dict(response.json())

    route_polyline = result['routes'][0]['overview_polyline']['points']

    query = """INSERT INTO driver_matchmaking_pool 
                    (user_id, trip_start_point, trip_end_point, destination_polyline, available_seat, trip_start_time)
                    VALUES ('%s', ST_SetSRID(ST_MakePoint(%f, %f), 4326), ST_SetSRID(ST_MakePoint(%f, %f), 4326), '%s', '%s', '%s')""" \
            % (user_id, float(start_lat), float(start_lon),
               float(end_lat), float(end_lon),
               route_polyline,
               available_seat, trip_start_time)

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
    start_lat, start_lon = tuple(request.json['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.json['trip_end_point'].split(','))
    trip_start_time = request.json['trip_start_time']

    direction_api_key = app.config["DIRECTIONS_API_KEY"]
    directions_base_url = 'https://maps.googleapis.com/maps/api/directions/json'
    url = directions_base_url + '?' + urllib.parse.urlencode({
        'origin': "%s,%s" % (start_lat, start_lon),
        'destination': "%s,%s" % (end_lat, end_lon),
        'key': direction_api_key,
    })

    response = requests.get(url)
    result = dict(response.json())

    route_polyline = result['routes'][0]['overview_polyline']['points']

    query = """INSERT INTO hitchhiker_matchmaking_pool 
                        (user_id, trip_start_point, trip_end_point, trip_start_time, destination_polyline)
                        VALUES ('%s', ST_GeomFromText('POINT(%f %f)', 4326), ST_GeomFromText('POINT(%f %f)', 4326), '%s', '%s')""" \
            % (user_id,
               float(start_lat), float(start_lon),
               float(end_lat), float(end_lon),
               trip_start_time, route_polyline)

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify(e)

    return jsonify(True)

def check_polylines_intersections(driver_poly, hitchikker_poly):
    driver_poly_decoded = polyline.decode(driver_poly)
    hitchikker_poly_decodesd = polyline.decode(hitchikker_poly)
    intersections = [value for value in driver_poly_decoded if value in hitchikker_poly_decodesd]
    return intersections



@route_matchmaking.route('/get_trip_hitchhiker', methods=['POST'])
def get_trip_hitchhiker():
    user_id = 1
    start_lat, start_lon = tuple(request.json['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.json['trip_start_point'].split(','))
    trip_start_time = request.form['trip_start_time']
    # route_polyline = request.form['route_polyline']

    query = """SELECT * 
                FROM driver_matchmaking_pool
                WHERE trip_start_point = ST_GeomFromText('POINT(%f %f)', 4326) AND 
                trip_end_point = ST_GeomFromText('POINT(%f %f)', 4326) """\
            % (float(start_lat), float(start_lon),
               float(end_lat), float(end_lon))

    conn = db_connection()
    result = execute_query(query, conn)

    if result:
        return jsonify(result)
    else:
        return jsonify(False)