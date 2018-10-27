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
        # read connection parameters

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USERNAME, password=DB_PASS)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
