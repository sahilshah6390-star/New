# database/connection.py

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "kasukabe.db")

db = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = db.cursor()