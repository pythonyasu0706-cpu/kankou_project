from dotenv import load_dotenv
import psycopg2
import os

# .envを読み込む
load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])

# conn = psycopg2.connect(
#     dbname="kankou-db",
#     user="kankou_user",
#     password="PDOfTzydtbQ0PortGZLjvfrWuc9Qrwnh",
#     host="postgresql://kankou_user:PDOfTzydtbQ0PortGZLjvfrWuc9Qrwnh@dpg-d7pngs7aqgkc738i16e0-a.oregon-postgres.render.com/kankou_db",
#     port="5432"
# )

cur = conn.cursor()

cur.execute("""
    ALTER TABLE contacts
    ADD COLUMN status VARCHAR(20) DEFAULT 'new';
""")

cur.execute("""
    UPDATE contacts
    SET status = 'new'
    WHERE status IS NULL;
""")

conn.commit()
cur.close()
conn.close()

print("完了")