import sqlite3
from datetime import datetime

DB_NAME = "rankings.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  roll_number TEXT,
                  name TEXT,
                  score REAL,
                  correct INTEGER,
                  wrong INTEGER,
                  timestamp DATETIME)''')
    conn.commit()
    conn.close()

def save_score(roll_number, name, score, correct, wrong):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Check if entry exists to update or insert
    c.execute("SELECT id FROM submissions WHERE roll_number=?", (roll_number,))
    existing = c.fetchone()
    
    timestamp = datetime.now()
    
    if existing:
        c.execute('''UPDATE submissions 
                     SET score=?, correct=?, wrong=?, timestamp=? 
                     WHERE roll_number=?''', 
                  (score, correct, wrong, timestamp, roll_number))
    else:
        c.execute('''INSERT INTO submissions (roll_number, name, score, correct, wrong, timestamp)
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                  (roll_number, name, score, correct, wrong, timestamp))
    
    conn.commit()
    conn.close()

def get_rank(score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Rank is 1 + count of people with higher score
    c.execute("SELECT count(*) FROM submissions WHERE score > ?", (score,))
    rank = c.fetchone()[0] + 1
    
    # Get total participants
    c.execute("SELECT count(*) FROM submissions")
    total = c.fetchone()[0]
    
    conn.close()
    return rank, total

def get_leaderboard(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, score, correct, wrong FROM submissions ORDER BY score DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    return data
