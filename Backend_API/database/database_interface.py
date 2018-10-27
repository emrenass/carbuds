import psycopg2
import psycopg2.extras
from Backend_API.database import database_config

DB_HOST = database_config.DB_HOST
DB_PORT = database_config.DB_PORT
DB_NAME = database_config.DB_NAME
DB_USERNAME = database_config.DB_USERNAME
DB_PASS = database_config.DB_PASS


def db_connection():
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USERNAME, password=DB_PASS)

    return conn


def execute_query(query, conn):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
    return rows


def commit_query(query, conn):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query)
        conn.commit()
        conn.close()
    return
