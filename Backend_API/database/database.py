import psycopg2
from Backend_API.database import database_config
from Backend_API.database import database_interface as din

DB_HOST = database_config.DB_HOST
DB_PORT = database_config.DB_PORT
DB_NAME = database_config.DB_NAME
DB_USERNAME = database_config.DB_USERNAME
DB_PASS = database_config.DB_PASS


def upload_tables():
    enums = create_enums()
    drop_table = drop_tables()
    tables = create_table()
    views = create_views()

    conn = din.db_connection()
    din.commit_query_multiple(views, conn)
    #din.commit_query_multiple(drop_table, conn)
    #din.commit_query_multiple(enums, conn)
    #din.commit_query_multiple(tables, conn)

    conn.close()


def create_enums():
    Gender_enum = """CREATE TYPE gender AS ENUM ('Male', 'Female');"""
    Music_enum = """CREATE TYPE music AS ENUM ('Electro', 'Pop', 'Rock', 'Rap');"""
    Profile_enum = """CREATE TYPE profile AS ENUM ('Driver', 'Hitchhiker');"""
    commands = [Gender_enum, Music_enum, Profile_enum]
    return commands


def create_table():
    Users = """ CREATE TABLE Users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                lastname VARCHAR(50),
                username VARCHAR(30) UNIQUE ,
                password VARCHAR(50),
                registration_date timestamp not null default CURRENT_TIMESTAMP,
                email VARCHAR(100) UNIQUE,
                gender gender,
                device_reg_id TEXT,
                current_profile profile
                )
            """

    Driver_profile = """CREATE TABLE Driver_profile (
                        user_id int UNIQUE,
                        car_model int,
                        license_plate VARCHAR(9),
                        hitchhiker_gender_preference gender[],
                        music_preference music[],
                        passenger_seat int,
                        CONSTRAINT Driver_profile_User_id_fk FOREIGN KEY (user_id) REFERENCES Users (id),
                        CONSTRAINT Driver_profile_model_id_fk FOREIGN KEY (car_model) REFERENCES Car_model (id)
                        );
                    """

    Hitchhiker_profile = """CREATE TABLE Hitchhiker_profile (
                            user_id int UNIQUE,
                            driver_gender_preference gender[],
                            music_preference music[],
                            CONSTRAINT Hitchhiker_profile_User_id_fk FOREIGN KEY (user_id) REFERENCES Users (id)
                            );
                        """

    Car_brand = """CREATE TABLE Car_brand (
                                id SERIAL PRIMARY KEY,
                                brand VARCHAR(30)
                                );
                            """

    Car_model = """CREATE TABLE Car_model (
                    id SERIAL PRIMARY KEY,
                    brand_id int,
                    model VARCHAR(30),
                    CONSTRAINT Car_model_brand_id_fk FOREIGN KEY (brand_id) REFERENCES Car_brand (id)
                )
                """

    Driver_matchmaking_pool = """CREATE TABLE Driver_matchmaking_pool (
                                    id SERIAL PRIMARY KEY,
                                    user_id int,
                                    available_seat int,
                                    trip_start_time timestamp,
                                    destination_polyline TEXT,
                                    CONSTRAINT Driver_matchmaking_pool_user_id_fk FOREIGN KEY (user_id) REFERENCES Users (id)
                                )
                                """

    Hitchhiker_matchmaking_pool = """CREATE TABLE Hitchhiker_matchmaking_pool (
                                       id SERIAL PRIMARY KEY,
                                       user_id int,
                                       trip_start_time timestamp,
                                       destination_polyline TEXT,
                                       CONSTRAINT Hitchhiker_matchmaking_pool_user_id_fk FOREIGN KEY (user_id) REFERENCES Users (id)
                                   )
                                   """
    possible_match_pool = """CREATE TABLE possible_match_pool (
                            match_id SERIAL PRIMARY KEY,
                            intersection_polyline TEXT,
                            hitchhiker_id int,
                            driver_id int,
                            trip_start_time timestamp,
                            is_driver_liked boolean,
                            is_hitchhiker_like boolean,
                            is_driver_liked boolean default false ,
                            is_hitchhiker_liked boolean default false,
                            is_matched boolean default false,
                            CONSTRAINT Driver_profile_User_id_fk FOREIGN KEY (driver_id) REFERENCES Users (id),
                            CONSTRAINT hitchhiker_profile_user_id_fk FOREIGN KEY (hitchhiker_id) REFERENCES Users (id)
                            );
                        """

    match_pool = """create table match_pool(
                    match_id SERIAL PRIMARY KEY,
                    intersection_polyline TEXT,
                    hitchhiker_id int,
                    driver_id int,
                    start_point TEXT,
                    end_point TEXT,
                    trip_start_time timestamp,
                    driver_name varchar(50),
                    driver_lastname varchar(50),
                    hitchhiker_name varchar(50),
                    hitchhiker_lastname varchar(50),
                    exchange_name TEXT,
                    hitchhiker_queue TEXT,
                    driver_queue TEXT,
                    CONSTRAINT Driver_profile_User_id_fk FOREIGN KEY (driver_id) REFERENCES Users (id),
                    CONSTRAINT hitchhiker_profile_user_id_fk FOREIGN KEY (hitchhiker_id) REFERENCES Users (id)
                    );"""

    Hitchhiker_matchmaking_pool_start = """SELECT AddGeometryColumn ('hitchhiker_matchmaking_pool','trip_start_point',4326,'POINT',2);
                                       """
    Hitchhiker_matchmaking_pool_end = """SELECT AddGeometryColumn ('hitchhiker_matchmaking_pool','trip_end_point',4326,'POINT',2);
                                           """
    Driver_matchmaking_pool_start = """SELECT AddGeometryColumn ('driver_matchmaking_pool','trip_start_point',4326,'POINT',2);
                                           """
    Driver_matchmaking_pool_end = """SELECT AddGeometryColumn ('driver_matchmaking_pool','trip_end_point',4326,'POINT',2);
                                               """

    commands = [Users, Car_brand, Car_model, Driver_profile, Hitchhiker_profile,
                Driver_matchmaking_pool, Hitchhiker_matchmaking_pool,
                Hitchhiker_matchmaking_pool_start, Hitchhiker_matchmaking_pool_end,
                Driver_matchmaking_pool_start, Driver_matchmaking_pool_end,
                possible_match_pool, match_pool]
    return commands


def drop_tables():
    Users = """DROP TABLE IF EXISTS Users CASCADE"""
    Driver_profile = """DROP TABLE IF EXISTS Driver_profile CASCADE"""
    Hitchhiker_profile = """DROP TABLE IF EXISTS Hitchhiker_profile CASCADE"""
    Car_brand = """DROP TABLE IF EXISTS Car_brand CASCADE"""
    Car_model = """DROP TABLE IF EXISTS Car_model CASCADE"""
    Driver_matchmaking_pool = """DROP TABLE IF EXISTS Driver_matchmaking_pool CASCADE"""
    Hitchhiker_matchmaking_pool = """DROP TABLE IF EXISTS Hitchhiker_matchmaking_pool CASCADE"""

    commands = [Users, Car_brand, Car_model, Driver_profile, Hitchhiker_profile, Driver_matchmaking_pool,
                Hitchhiker_matchmaking_pool]
    return commands


def create_views():
    hitchhiker_matchmaking = """CREATE VIEW  hitchhiker_matchmaking AS
    SELECT u.id, hm.trip_start_time, hm.destination_polyline, hm.trip_start_point, hm.trip_end_point, hp.driver_gender_preference, hp.music_preference
    FROM hitchhiker_matchmaking_pool hm
        inner join
    users u
        on u.id = hm.user_id
        inner join
    hitchhiker_profile hp
        on hm.user_id = hp.user_id;"""

    driver_matchmaking = """CREATE VIEW  driver_matchmaking AS
    SELECT u.id, dm.trip_start_time, dm.destination_polyline, dm.trip_start_point, dm.trip_end_point, dp.hitchhiker_gender_preference, dp.music_preference
    FROM driver_matchmaking_pool dm
            inner join
        users u
            on u.id = dm.user_id
            inner join
        driver_profile dp
        on dm.user_id = dp.user_id;"""

    commands = [hitchhiker_matchmaking, driver_matchmaking]
    return commands

if __name__ == '__main__':
    upload_tables()
