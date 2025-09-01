import sqlite3
from pathlib import Path

DB_FILE = Path("plans.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Students
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    accommodations TEXT,
                    iep_link TEXT
                 )''')
    # Weekly plans
    c.execute('''CREATE TABLE IF NOT EXISTS plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week TEXT,
                    student_id INTEGER,
                    lesson TEXT,
                    activity TEXT,
                    mastery TEXT,
                    FOREIGN KEY(student_id) REFERENCES students(id)
                 )''')
    # Historical reports
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    summary TEXT
                 )''')
    conn.commit()
    conn.close()

def add_student(name, accommodations, iep_link):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO students (name, accommodations, iep_link) VALUES (?, ?, ?)",
              (name, accommodations, iep_link))
    conn.commit()
    conn.close()

def save_plan(week, student_id, lesson, activity, mastery):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO plans (week, student_id, lesson, activity, mastery) VALUES (?, ?, ?, ?, ?)",
              (week, student_id, lesson, activity, mastery))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    return rows

def get_plans(week=None, student_id=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM plans WHERE 1=1"
    params = []
    if week:
        query += " AND week=?"
        params.append(week)
    if student_id:
        query += " AND student_id=?"
        params.append(student_id)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows
