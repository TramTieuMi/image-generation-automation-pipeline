import sqlite3
import json
from datetime import datetime
import os

DB_PATH = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS task_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            format TEXT,
            model TEXT,
            example_urls TEXT,
            asset_url TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_request(description: str, fmt: str, model: str, example_urls: list, asset_url: str, status: str):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO task_logs 
        (description, format, model, example_urls, asset_url, status, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        description, fmt, model, json.dumps(example_urls),
        asset_url, status, datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

    