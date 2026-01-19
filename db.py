import sqlite3
from sqlite3 import Connection, Cursor

DB_NAME = 'hiring.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT NOT NULL,
        applied_date TEXT NOT NULL
    )
    """);
    
    # Pipeline stages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_stages (
        stage_id INTEGER PRIMARY KEY,
        stage_name TEXT NOT NULL
    )
    """)

    # Candidate stage history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_stage_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        stage_id INTEGER,
        updated_at TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id),
        FOREIGN KEY(stage_id) REFERENCES pipeline_stages(stage_id)
    )
    """)

    # Interviews table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        interviewer TEXT,
        score INTEGER,
        feedback TEXT,
        interview_date TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id)
    )
    """)

    # Rejections table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rejections (
        rejection_id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        reason TEXT,
        rejected_at TEXT,
        FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id)
    )
    """)
    
    conn.commit();
    conn.close()
    
def seed_pipeline_stages():
    conn = get_connection()
    cursor = conn.cursor()

    stages = [
        (1, "Applied"),
        (2, "Screening"),
        (3, "Interview"),
        (4, "Offer"),
        (5, "Hired"),
        (6, "Rejected")
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO pipeline_stages (stage_id, stage_name)
    VALUES (?, ?)
    """, stages)

    conn.commit()
    conn.close()
