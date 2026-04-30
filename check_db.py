from db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM contacts ORDER BY created_at DESC")
rows = cur.fetchall()

print(rows)

conn.close()