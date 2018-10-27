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

    conn = din.db_connection()

    din.commit_query_multiple(drop_table, conn)
    #din.commit_query_multiple(enums, conn)
    din.commit_query_multiple(tables, conn)

    conn.close()



def create_enums():
    Gender_enum = """CREATE TYPE gender AS ENUM ('Male', 'Female', 'Both');"""
    Music_enum = """CREATE TYPE music AS ENUM ('Electro', 'Pop', 'Rock', 'Rap');"""
    commands = [Gender_enum,Music_enum]
    return commands

def create_table():


    User = """ CREATE TABLE "User" (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                lastname VARCHAR(50),
                username VARCHAR(30) UNIQUE ,
                password VARCHAR(50),
                registration_date timestamp not null default CURRENT_TIMESTAMP,
                email VARCHAR(100) UNIQUE 
                )
            """

    Driver_profile = """CREATE TABLE Driver_profile (
                        user_id int,
                        car_model int,
                        license_plate VARCHAR(9),
                        hitchhiker_gender_preference gender,
                        music_prefrence music[],

                        CONSTRAINT Driver_profile_User_id_fk FOREIGN KEY (user_id) REFERENCES "User" (id),
                        CONSTRAINT Driver_profile_model_id_fk FOREIGN KEY (car_model) REFERENCES Car_model (id)
                        );
                    """

    Hitchhiker_profile = """CREATE TABLE Hitchhiker_profile (
                            user_id int,
                            driver_gender_preference gender,
                            music_prefrence music[],
                            CONSTRAINT Hitchhiker_profile_User_id_fk FOREIGN KEY (user_id) REFERENCES "User" (id)
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

    commands = [User, Car_brand, Car_model, Driver_profile, Hitchhiker_profile]
    return commands

def drop_tables():
    User = """DROP TABLE IF EXISTS "User" CASCADE"""
    Driver_profile = """DROP TABLE IF EXISTS Driver_profile CASCADE"""
    Hitchhiker_profile = """DROP TABLE IF EXISTS Hitchhiker_profile CASCADE"""
    Car_brand = """DROP TABLE IF EXISTS Car_brand CASCADE"""
    Car_model = """DROP TABLE IF EXISTS Car_model CASCADE"""

    commands = [User, Car_brand, Car_model, Driver_profile, Hitchhiker_profile]
    return commands


if __name__ == '__main__':
    upload_tables()