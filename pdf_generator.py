from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db import get_students, get_plans
from pathlib import Path

PDF_FOLDER = Path("pdfs")
PDF_FOLDER.mkdir(exist_ok=True)

def generate_student_pdf(student_id, week):
    student = [s for s in get_students() if s[0] == student_id][0]
    plans = get_plans(week=week, student_id=student_id)
    
    filename = PDF_FOLDER / f"{student[1]}_{week}.pdf"
    c = canvas.Canvas(str(filename), pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, f"Weekly Lesson Plan for {student[1]}")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"IEP Link: {student[3]}")
    c.drawString(50, 710, f"Accommodations: {student[2]}")
    c.drawString(50, 690, f"Week: {week}")

    y = 660
    for p in plans:
        c.drawString(50, y, f"Lesson: {p[3]}, Activity: {p[4]}, Mastery: {p[5]}")
        y -= 20

    c.save()
    return filename
