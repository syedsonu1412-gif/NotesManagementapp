import sqlite3

DATABASE = "notes.db"
SCHEMA_FILE = "schema.sql"

def init_db():
 conn = sqlite3.connect(DATABASE)
 with open(SCHEMA_FILE, "r") as f:
  conn.executescript(f.read())
 conn.commit()
 conn.close()
 print("✅ Database initialized successfully.")

if __name__ == "__main__":
 init_db()