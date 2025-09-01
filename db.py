# db.py (fixed with subject column)
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
    # Plans with subject - FIXED SCHEMA
    c.execute('''CREATE TABLE IF NOT EXISTS plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week TEXT,
                    student_id INTEGER,
                    subject TEXT,  # Added this column
                    lesson_id TEXT,
                    detailed_plan TEXT,
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

# ... rest of the functions remain the same ...

def add_student(name, accommodations, iep_link):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO students (name, accommodations, iep_link) VALUES (?, ?, ?)",
              (name, accommodations, iep_link))
    conn.commit()
    conn.close()

def save_plan(week, student_id, subject, lesson_id, detailed_plan, mastery):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO plans (week, student_id, subject, lesson_id, detailed_plan, mastery) VALUES (?, ?, ?, ?, ?, ?)",
              (week, student_id, subject, lesson_id, detailed_plan, mastery))
    conn.commit()
    conn.close()

def get_students():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    return rows

def get_plans(week=None, student_id=None, subject=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Build query dynamically based on provided filters
    query = "SELECT * FROM plans"
    conditions = []
    params = []
    
    if week:
        conditions.append("week = ?")
        params.append(week)
    if student_id:
        conditions.append("student_id = ?")
        params.append(student_id)
    if subject:
        conditions.append("subject = ?")
        params.append(subject)
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def get_next_lesson(student_id, subject, lessons_df):
    plans = get_plans(student_id=student_id, subject=subject)
    mastered = [p[4] for p in plans if p[6] == "Mastered"]
    all_lessons = lessons_df['Lesson_ID'].tolist()
    for lesson in all_lessons:
        if lesson not in mastered:
            return lesson
    return all_lessons[0]  # Cycle back for review

def has_plans_for_week(week):
    plans = get_plans(week=week)
    return len(plans) > 0
