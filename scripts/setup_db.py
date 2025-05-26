import sqlite3
from lib.db.connection import get_connection

# Script to set up the database schema

def setup_db():
    conn = get_connection()
    with open('lib/db/schema.sql', 'r') as f:
        sql = f.read()
    try:
        with conn:
            conn.executescript(sql)
        print("Database schema created.")
    finally:
        conn.close()

if __name__ == "__main__":
    setup_db()
