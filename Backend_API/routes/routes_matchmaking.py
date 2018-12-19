from datetime import datetime

import jwt
from flask import request, make_response, render_template, Blueprint, jsonify, redirect
from flask import current_app as app
from Backend_API.utils.decorators import login_required
from Backend_API.database.database_interface import *
import urllib.parse
import requests
import polyline
import googlemaps

route_matchmaking = Blueprint('route_matchmaking', __name__)


@route_matchmaking.route('/set_trip_driver', methods=['POST'])
@login_required
def set_trip_driver():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
    start_lat, start_lon = tuple(request.json['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.json['trip_end_point'].split(','))
    trip_start_time = request.json['trip_start_time']
    available_seat = request.json['available_seat']

    gmaps = googlemaps.Client(key=app.config["DIRECTIONS_API_KEY"])

    directions_result = gmaps.directions("%s, %s" % (start_lat, start_lon),
                                         "%s, %s" % (end_lat, end_lon),
                                         mode="transit",
                                         units='metric',
                                         departure_time=datetime.now())

    if not directions_result:
        return jsonify("No Available Route")
    route_polyline = directions_result[0]['overview_polyline']['points']

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
        return "Database Error"

    find_and_write_hitchhiker_candidates(user_id)

    return jsonify(True)


@route_matchmaking.route('/set_trip_hitchhiker', methods=['POST'])
@login_required
def set_trip_hitchhiker():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
    start_lat, start_lon = tuple(request.json['trip_start_point'].split(','))
    end_lat, end_lon = tuple(request.json['trip_end_point'].split(','))
    trip_start_time = request.json['trip_start_time']

    gmaps = googlemaps.Client(key=app.config["DIRECTIONS_API_KEY"])

    directions_result = gmaps.directions("%s, %s" % (start_lat, start_lon),
                                         "%s, %s" % (end_lat, end_lon),
                                         mode="transit",
                                         units='metric',
                                         departure_time=datetime.now())

    if not directions_result:
        return jsonify("No Available Route")

    route_polyline = directions_result[0]['overview_polyline']['points']

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
        return "Database Error"
    find_and_write_driver_candidates(user_id)
    return jsonify(True)


def check_polylines_intersections(driver_poly, hitchikker_poly):
    driver_poly_decoded = polyline.decode(driver_poly)
    hitchikker_poly_decodesd = polyline.decode(hitchikker_poly)
    intersections = [value for value in driver_poly_decoded if value in hitchikker_poly_decodesd]
    return intersections


def polyline_encoder(coord_list):
    return polyline.encode(coord_list)


@route_matchmaking.route('/get_driver_candidate', methods=['POST'])
@login_required
def get_driver_candidate():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']

    query = """SELECT *
                FROM possible_match_pool
                INNER JOIN users on possible_match_pool.driver_id = users.id
                WHERE hitchhiker_id = %s """ % user_id
    try:
        conn = db_connection()
        hitch_result = execute_query(query, conn)
    except Exception as e:
        print(e)
        return "Database Error"
    if hitch_result:
        return jsonify(hitch_result)
    return jsonify(False)


@route_matchmaking.route('/get_hitchhiker_candidate', methods=['POST'])
@login_required
def get_hitchhiker_candidate():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']

    query = """SELECT *
                    FROM possible_match_pool
                    INNER JOIN users on possible_match_pool.hitchhiker_id = users.id
                    WHERE driver_id = %s """ % user_id
    try:
        conn = db_connection()
        hitch_result = execute_query(query, conn)
    except Exception as e:
        print(e)
        return "Database Error"
    if hitch_result:
        return jsonify(hitch_result)
    return jsonify(False)


@route_matchmaking.route('/cancel_driver_trip', methods=['POST'])
@login_required
def cancel_driver_trip():
    trip_id = request.json['trip_id']

    query = """DELETE FROM driver_matchmaking_pool
                WHERE id = %s """ % trip_id
    try:
        conn = db_connection()
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return "Database Error"

    return jsonify(True)


@route_matchmaking.route('/cancel_hitchhiker_trip', methods=['POST'])
@login_required
def cancel_hitchhiker_trip():
    trip_id = request.json['trip_id']

    query = """DELETE 
                FROM hitchhiker_matchmaking_pool
                WHERE id = %s """ % trip_id
    try:
        conn = db_connection()
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return "Database Error"

    return jsonify(True)


@route_matchmaking.route('/dislike_match', methods=['POST'])
@login_required
def dislike_match():
    possible_match_id = request.json['possible_match_id']

    query = """DELETE 
                FROM possible_match_pool
                WHERE match_id = %s""" % possible_match_id

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify("Database Error")
    return jsonify(True)


@route_matchmaking.route('/like_match', methods=['POST'])
@login_required
def like_match():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']
    possible_match_id = request.json['possible_match_id']

    query = """UPDATE possible_match_pool
                    SET is_driver_liked = case 
                                          when driver_id = %s then True
                                          else is_driver_liked
                                          end,
                    is_hitchhiker_like = case 
                                          when hitchhiker_id = %s then True
                                          else is_hitchhiker_like
                                          end
                    WHERE match_id = %s""" % (user_id, user_id, possible_match_id)

    conn = db_connection()

    try:
        commit_query(query, conn)
    except Exception as e:
        print(e)
        return jsonify("Database Error")
    return jsonify(True)


@route_matchmaking.route('/get_matches', methods=['POST'])
def get_matches():
    token = jwt.decode(request.json['token'], app.config['SECRET_KEY'], algorithm=['HS256'])
    user_id = token['user_id']

    query = """SELECT *
                FROM match_pool
                WHERE hitchhiker_id = %s OR driver_id = %s""" % (user_id, user_id)
    try:
        conn = db_connection()
        match_result = execute_query(query, conn)
    except Exception as e:
        print(e)
        return "Database Error"

    return jsonify(match_result)


@route_matchmaking.route('/remove_match', methods=['POST'])
@login_required
def remove_match():
    pass


@route_matchmaking.route('/finish_match', methods=['POST'])
@login_required
def finish_match():
    pass


def find_and_write_driver_candidates(user_id):
    query = """SELECT destination_polyline, trip_start_time,
                    ST_X(trip_start_point) lat_start, ST_Y(trip_start_point) lon_start,
                    hitchhiker_profile.music_preference, hitchhiker_profile.driver_gender_preference
                    FROM hitchhiker_matchmaking_pool
                    INNER JOIN hitchhiker_profile
                    ON hitchhiker_matchmaking_pool.user_id = hitchhiker_profile.user_id
                    WHERE hitchhiker_matchmaking_pool.user_id = %s """ % user_id
    try:
        conn = db_connection()
        hitch_result = execute_query(query, conn)
    except Exception as e:
        print(e)
        return "Database Error"

    for trip in hitch_result:
        try:
            start_lat = trip['lat_start']
            start_lon = trip['lon_start']
            music_pref = trip['music_preference']
            gender_pref = trip['driver_gender_preference']
            trip_start_time = trip['trip_start_time']
            hitchhiker_route_polyline = trip['destination_polyline']
        except Exception as e:
            print(e)
            return "User Does Not Exist"

        query = """SELECT * 
                        FROM driver_matchmaking_pool
                        INNER JOIN driver_profile
                        ON driver_matchmaking_pool.user_id = driver_profile.user_id
                        WHERE  ST_Distance_Sphere(trip_start_point, ST_MakePoint(%f, %f)) <= 1 * 1000 AND
                                '%s' && driver_profile.music_preference AND 
                                ((SELECT gender from users where id=%s) || ARRAY[]::gender[]) && driver_profile.hitchhiker_gender_preference AND
                                driver_matchmaking_pool.trip_start_time <= (timestamp '%s' + interval '1 hours')""" \
                % (float(start_lat), float(start_lon),
                   music_pref, user_id, trip_start_time)

        try:
            conn = db_connection()
            driver_result = execute_query(query, conn)
        except Exception as e:
            print(e)
            return "Database Error"

        try:
            gmaps = googlemaps.Client(key=app.config["DIRECTIONS_API_KEY"])
            for candidate in driver_result:
                driver_polyline = candidate['destination_polyline']
                intersection_polyline = check_polylines_intersections(driver_polyline, hitchhiker_route_polyline)

                if not intersection_polyline:
                    continue

                inter_start_lat, inter_start_lon = intersection_polyline[0]
                inter_end_lat, inter_end_lon = intersection_polyline[-1]

                distance_result = gmaps.distance_matrix("%s, %s" % (inter_start_lat, inter_start_lon),
                                                        "%s, %s" % (inter_end_lat, inter_end_lon),
                                                        mode="transit",
                                                        units='metric',
                                                        departure_time=datetime.now())

                intersection_distance = distance_result['rows'][0]['elements'][0]['distance']['value']

                if intersection_distance >= 1000:
                    candidate['intersection_polyline'] = polyline_encoder(intersection_polyline)
                    candidate['intersection_distance'] = intersection_distance
                    query = """INSERT INTO possible_match_pool 
                                    (intersection_polyline, hitchhiker_id, driver_id, trip_start_time)
                                    VALUES ('%s', '%s', '%s', '%s')""" \
                            % (candidate['intersection_polyline'], user_id, candidate['user_id'], trip_start_time)

                    try:
                        conn = db_connection()
                        commit_query(query, conn)
                    except Exception as e:
                        print(e)
                        return "Database Error"
        except Exception as e:
            print(e)
            return "Google Maps API Error"


def find_and_write_hitchhiker_candidates(user_id):
    query = """SELECT destination_polyline, trip_start_time,
                        ST_X(trip_start_point) lat_start, ST_Y(trip_start_point) lon_start,
                        driver_profile.music_preference, driver_profile.hitchhiker_gender_preference
                        FROM driver_matchmaking_pool
                        INNER JOIN driver_profile
                        ON driver_matchmaking_pool.user_id = driver_profile.user_id
                        WHERE driver_matchmaking_pool.user_id = %s """ % user_id

    try:
        conn = db_connection()
        driver_result = execute_query(query, conn)
    except:
        return "Database Error"

    for trip in driver_result:
        try:
            start_lat = trip['lat_start']
            start_lon = trip['lon_start']
            music_pref = trip['music_preference']
            gender_pref = trip['hitchhiker_gender_preference']
            trip_start_time = trip['trip_start_time']
            hitchhiker_route_polyline = trip['destination_polyline']
        except Exception as e:
            print(e)
            return "User Does Not Exist"

        query = """SELECT * 
                            FROM hitchhiker_matchmaking_pool
                            INNER JOIN hitchhiker_profile
                            ON hitchhiker_matchmaking_pool.user_id = hitchhiker_profile.user_id
                            WHERE  ST_Distance_Sphere(trip_start_point, ST_MakePoint(%f, %f)) <= 1 * 1000 AND
                            '%s' && hitchhiker_profile.music_preference AND 
                            ((SELECT gender from users where id=%s) || ARRAY[]::gender[]) && hitchhiker_profile.driver_gender_preference """ \
                % (float(start_lat), float(start_lon),
                   music_pref, user_id)

        try:
            conn = db_connection()
            hitch_result = execute_query(query, conn)
        except:
            return "Database Error"

        try:
            gmaps = googlemaps.Client(key=app.config["DIRECTIONS_API_KEY"])
            for candidate in hitch_result:
                driver_polyline = candidate['destination_polyline']
                intersection_polyline = check_polylines_intersections(driver_polyline, hitchhiker_route_polyline)

                if not intersection_polyline:
                    continue

                inter_start_lat, inter_start_lon = intersection_polyline[0]
                inter_end_lat, inter_end_lon = intersection_polyline[-1]

                distance_result = gmaps.distance_matrix("%s, %s" % (inter_start_lat, inter_start_lon),
                                                        "%s, %s" % (inter_end_lat, inter_end_lon),
                                                        mode="transit",
                                                        units='metric',
                                                        departure_time=datetime.now())

                intersection_distance = distance_result['rows'][0]['elements'][0]['distance']['value']

                if intersection_distance >= 1000:
                    candidate['intersection_polyline'] = polyline_encoder(intersection_polyline)
                    candidate['intersection_distance'] = intersection_distance
                    query = """INSERT INTO possible_match_pool 
                                    (intersection_polyline, hitchhiker_id, driver_id, trip_start_time)
                                    VALUES ('%s', '%s', '%s', '%s')""" \
                            % (candidate['intersection_polyline'], candidate['user_id'], user_id, trip_start_time)

                    try:
                        conn = db_connection()
                        commit_query(query, conn)
                    except Exception as e:
                        print(e)
                        return "Database Error"
        except Exception as e:
            print(e)
            return "Google Maps API Error"
