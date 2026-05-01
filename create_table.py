from dotenv import load_dotenv
from db import get_db_connection
import psycopg2
import os
load_dotenv()

def create_table():
    print(os.environ.get("DATABASE_URL"))
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE contacts (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        tel TEXT,
        address TEXT,
        title TEXT,
        note TEXT,
        catalog TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("テーブル作成完了")

if __name__ == "__main__":
    create_table()