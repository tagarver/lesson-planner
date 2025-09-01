from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db import get_students, get_plans
from pathlib import Path
from datetime import datetime, timedelta

PDF_FOLDER = Path("pdfs")
PDF_FOLDER.mkdir(exist_ok=True)

def generate_student_pdf(student_id, week):
    student = [s for s in get_students() if s[0] == student_id][0]
    plans = get_plans(week=week, student_id=student_id)
    
    filename = PDF_FOLDER / f"{student[1]}_{week}.pdf"
    c = canvas.Canvas(str(filename), pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, f"Weekly Lesson Plan for {student[1]} - Week: {week}")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"IEP Link: {student[3]}")
    c.drawString(50, 710, f"Accommodations: {student[2]}")

    # Daily breakdown
    start_date = datetime.strptime(week.split(' to ')[0], '%Y-%m-%d')
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    y = 680
    for i, day in enumerate(days):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        c.drawString(50, y, f"{day} ({date}):")
        y -= 20
        for p in plans:
            if p[3] == 'Life Skills':
                c.drawString(60, y, "7:05-8:30 Life Skills:")
                y -= 15
            elif p[3] == 'Literacy (ULS)':
                c.drawString(60, y, "9:20-10:20 Literacy:")
                y -= 15
            elif p[3] == 'Math (Coins/Expressions)':
                c.drawString(60, y, "Math:")
                y -= 15
            c.drawString(70, y, f"Lesson: {p[4]} (Mastery: {p[6]}) - Standard: {p[5].split('Standard: ')[-1]}")
            y -= 15
            for line in p[5].split('\n')[:-1]:  # Objectives, Materials, Steps
                c.drawString(80, y, line)
                y -= 15
        y -= 20 if i < 4 else 0

    c.save()
    return filename