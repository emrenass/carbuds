from Backend_API.database.database_interface import *
from Backend_API.utils.carbuds_config import *
from Backend_API.rabbitmq.rabbitmq_interface import *
from Notification_Server.config import *

import googlemaps
import polyline
import pandas as pd
from _datetime import datetime
from time import sleep
from pyfcm import FCMNotification


def check_polylines_intersections(driver_poly, hitchikker_poly):
    driver_poly_decoded = polyline.decode(driver_poly)
    hitchikker_poly_decodesd = polyline.decode(hitchikker_poly)
    intersections = [value for value in driver_poly_decoded if value in hitchikker_poly_decodesd]
    return intersections


def polyline_encoder(coord_list):
    return polyline.encode(coord_list)


def polyline_decoder(poly):
    return polyline.decode(poly)


def match_possible_trip():
    while True:

        query = """select *
                    from possible_match_pool
                    where possible_match_pool.is_driver_liked = true and 
                    possible_match_pool.is_hitchhiker_like = true and
                    is_matched = false"""
        try:
            conn = db_connection()
            match_list = execute_query(query, conn)
        except Exception as e:
            print(e)
            continue

        if not match_list:
            print("No Matches Available Freezing 10 Seconds")
            sleep(10)  # Sleep 10 seconds when no matches available
            continue

        possible_matches_to_remove = []
        for match in match_list:
            possible_matches_to_remove.append(match['match_id'])

            hitchhiker, driver = prepare_user_information(match['hitchhiker_id'], match['driver_id'])
            exchange_name, hitchhiker_queue, driver_queue = init_message_room_for_match(match['match_id'])

            intersection_points = polyline.decode(match['intersection_polyline'])
            start_point = str(intersection_points[0])
            end_point = str(intersection_points[-1])

            query = """insert into match_pool 
                        (hitchhiker_id, driver_id,
                            intersection_polyline,
                            start_point, end_point,
                            trip_start_time,
                            driver_name, driver_lastname,
                            hitchhiker_name, hitchhiker_lastname,
                            exchange_name, hitchhiker_queue, driver_queue) 
                       values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                        % (match['hitchhiker_id'], match['driver_id'],
                           match['intersection_polyline'],
                           start_point, end_point,
                           match['trip_start_time'],
                           driver['name'], driver['lastname'],
                           hitchhiker['name'], hitchhiker['lastname'],
                           exchange_name, hitchhiker_queue, driver_queue)
            try:
                conn = db_connection()
                commit_query(query, conn)
            except Exception as e:
                print(e)
                print("Database Error")
                continue
            try:
                push_match_notification(hitchhiker['device_reg_id'])
                push_match_notification(driver['device_reg_id'])
            except Exception as e:
                print(e.with_traceback)
                continue

        remove_from_possible_match(possible_matches_to_remove)
        print('Possible Matches Handled')


def remove_from_possible_match(possible_matches_to_remove):
    for id in possible_matches_to_remove:
        query = """update possible_match_pool
                    set is_matched = true
                   where match_id = %s""" % id
        try:
            conn = db_connection()
            commit_query(query, conn)
        except Exception as e:
            print(e)
            return "Database Error"
        print('Match ID %s Is Matched' % id)


def prepare_user_information(hitchhiker_id, driver_id):
    query = """select "name", lastname, device_reg_id
                from users
                where id = %s """ % hitchhiker_id
    try:
        conn = db_connection()
        hitchhiker_info = execute_query(query, conn)
    except Exception as e:
        raise e

    query = """select "name", lastname, device_reg_id
                from users
                where id = %s """ % driver_id
    try:
        conn = db_connection()
        driver_info = execute_query(query, conn)
    except Exception as e:
        raise e

    return hitchhiker_info[0], driver_info[0]


def init_message_room_for_match(possible_match_id):
    rabbitmq_conn = connection()
    exchange_name = 'chatroom_' + str(possible_match_id)
    exchange_initialize(rabbitmq_conn, exchange_name)

    hitchhiker_queue = init_queue(rabbitmq_conn, exchange_name)
    driver_queue = init_queue(rabbitmq_conn, exchange_name)

    rabbitmq_conn.close()
    return exchange_name, hitchhiker_queue, driver_queue


def push_match_notification(device_reg_id=None):

    push_service = FCMNotification(api_key=FCM_SERVER_KEY)

    if not device_reg_id:
        device_reg_id = "cYAYeJQosbo:APA91bEyFvhJml534sMe6eIPAZ2mVd6DR9Dw72GHBvzr9qWJkZbdcTwfYIEB34fvvqmOnpBt3Ud-8Be3oN-y_q14N39nBWfmhov984S1noIYpnqvLdeeQYVrkCOALLoCFFtMnuwAJ3hp"
    message_title = "CarBuds"
    message_body = "Hey! You Have a New CarBud!"

    try:
        result = push_service.notify_single_device(registration_id=device_reg_id,
                                                   message_title=message_title,
                                                   message_body=message_body)
    except Exception as e:
        raise e
    print("Notification Sent")


match_possible_trip()
