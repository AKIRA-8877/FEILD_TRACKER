import sqlite3
import os

db_path = 'instance/tracker.db'
sql_path = 'database.sql'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    with open(sql_path, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    conn.close()
    print(f"Database exported to {sql_path}")
else:
    print(f"Database {db_path} not found.")
