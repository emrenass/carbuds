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
    user_id = request.json['user_id']
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
    user_id = request.json['user_id']
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



@route_matchmaking.route('/get_driver_candidate', methods=['POST'])
def get_driver_candidate():
    user_id = request.json['user_id']

    query = """SELECT destination_polyline, trip_start_time,
                ST_X(trip_start_point) lat_start, ST_Y(trip_start_point) lon_start,
                hitchhiker_profile.music_prefrence, hitchhiker_profile.hitchhiker_gender_preference
                FROM hitchhiker_matchmaking_pool
                INNER JOIN hitchhiker_profile
                ON hitchhiker_matchmaking_pool.user_id = hitchhiker_profile.user_id
                WHERE hitchhiker_matchmaking_pool.user_id = %s """ \
            % (user_id)

    conn = db_connection()
    result = execute_query(query, conn)

    start_lat = result[0]['lat_start']
    start_lon = result[0]['lon_start']
    music_pref = result[0]['music_preference']
    gender_pref = result[0]['hitchhiker_gender_preference']
    trip_start_time = result[0]['trip_start_time']
    route_polyline = result[0]['destination_polyline']

    query = """SELECT * 
                FROM driver_matchmaking_pool
                INNER JOIN driver_profile
                ON driver_matchmaking_pool.user_id = driver_profile.user_id
                WHERE  ST_Distance_Sphere(trip_start_point, ST_MakePoint(%f, %f)) <= 1 * 1000 AND
                        driver_profile.music_prefrence = '%s' AND 
                        driver_profile.hitchhiker_gender_preference = '%s' """\
            % (float(start_lat), float(start_lon),
               music_pref, gender_pref)

    conn = db_connection()
    result = execute_query(query, conn)

    if result:
        return jsonify(result)
    else:
        return jsonify(False)


@route_matchmaking.route('/get_hitchhiker_candidate', methods=['POST'])
def get_hitchhiker_candidate():
    user_id = request.json['user_id']

    query = """SELECT destination_polyline, trip_start_time,
                    ST_X(trip_start_point) lat_start, ST_Y(trip_start_point) lon_start,
                    driver_profile.music_prefrence, driver_profile.hitchhiker_gender_preference
                    FROM driver_matchmaking_pool
                    INNER JOIN driver_profile
                    ON driver_matchmaking_pool.user_id = driver_profile.user_id
                    WHERE driver_matchmaking_pool.user_id = %s """ \
            % (user_id)

    conn = db_connection()
    result = execute_query(query, conn)

    if result:
        start_lat = result[0]['lat_start']
        start_lon = result[0]['lon_start']
        music_pref = result[0]['music_prefrence']
        gender_pref = result[0]['hitchhiker_gender_preference']
        trip_start_time = result[0]['trip_start_time']
        route_polyline = result[0]['destination_polyline']

        query = """SELECT * 
                        FROM hitchhiker_matchmaking_pool
                        INNER JOIN hitchhiker_profile
                        ON hitchhiker_matchmaking_pool.user_id = hitchhiker_profile.user_id
                        WHERE  ST_Distance_Sphere(trip_start_point, ST_MakePoint(%f, %f)) <= 1 * 1000 AND
                                hitchhiker_profile.music_prefrence = '%s' AND 
                                hitchhiker_profile.driver_gender_preference = '%s' """ \
                % (float(start_lat), float(start_lon),
                   music_pref, gender_pref)

        conn = db_connection()
        result = execute_query(query, conn)
    else:
        return jsonify(False)

    if result:
        return jsonify(result)
    else:
        return jsonify(False)