# database/users.py

import time
from database.connection import db, cur

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    joined_at INTEGER,
    last_seen INTEGER
)
""")
db.commit()


def track_user(user):
    uid = user.id
    username = user.username or ""
    first_name = user.first_name or ""
    now = int(time.time())

    cur.execute("SELECT user_id FROM users WHERE user_id=?", (uid,))
    exists = cur.fetchone()

    if exists is None:
        cur.execute(
            """
            INSERT INTO users (user_id, username, first_name, joined_at, last_seen)
            VALUES (?, ?, ?, ?, ?)
            """,
            (uid, username, first_name, now, now)
        )
    else:
        cur.execute(
            """
            UPDATE users
            SET username=?, first_name=?, last_seen=?
            WHERE user_id=?
            """,
            (username, first_name, now, uid)
        )

    db.commit()


def total_users():
    cur.execute("SELECT COUNT(*) FROM users")
    return cur.fetchone()[0]