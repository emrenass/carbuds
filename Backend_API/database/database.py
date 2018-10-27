import psycopg2
from Backend_API.database import database_config

DB_HOST = database_config.DB_HOST
DB_PORT = database_config.DB_PORT
DB_NAME = database_config.DB_NAME
DB_USERNAME = database_config.DB_USERNAME
DB_PASS = database_config.DB_PASS

conn = None

def connect():
    """ Connect to the PostgreSQL database server """
    global conn
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USERNAME, password=DB_PASS)

        cur = conn.cursor()

        commands = create_table()
        for values in commands.values():
            print(values)
            cur.execute(values)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def create_table():
    User = """ CREATE TABLE "user" (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50),
                lastname VARCHAR(50),
                username VARCHAR(30),
                password VARCHAR(50),
                registration_date date,
                email VARCHAR(100)
                )
        """

    commands = {
        "User": User
    }
    return commands


if __name__ == '__main__':
    connect()
