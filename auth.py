import sqlite3
import bcrypt

from datetime import datetime, date

def log_query(username, tool):
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO query_log (username, tool, timestamp) VALUES (?, ?, ?)",
              (username, tool, timestamp))
    conn.commit()
    conn.close()

def get_user_query_count_today(username):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(*) FROM query_log 
        WHERE username = ? AND date(timestamp) = ?
    ''', (username, today))
    count = c.fetchone()[0]
    conn.close()
    return count

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username, role, CAST(daily_limit AS INTEGER) FROM users")
    users = c.fetchall()
    conn.close()
    return users

def update_user_limit(username, new_limit):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET daily_limit = ? WHERE username = ?", (new_limit, username))
    conn.commit()
    conn.close()

def delete_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()
    
DB_PATH = "users.db"
def init_query_log():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS query_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    tool TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT,
                    role TEXT DEFAULT 'user',
                    daily_limit INTEGER DEFAULT 20
                )''')
    conn.commit()
    conn.close()
    init_query_log()

def add_user(username, password, role='user', daily_limit=20):
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, role, daily_limit) VALUES (?, ?, ?, ?)",
              (username, password_hash, role, daily_limit))
    conn.commit()
    conn.close()

def authenticate(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_hash, role = result
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True, role
    return False, None