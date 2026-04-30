import psycopg2
import psycopg2.extras
import os

def get_db_connection():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def get_dict_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
