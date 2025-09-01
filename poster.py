from PIL import Image, ImageDraw, ImageFont
from db import get_plans, get_students
from pathlib import Path
import json

POSTER_FOLDER = Path("posters")
POSTER_FOLDER.mkdir(exist_ok=True)
STATIC_FOLDER = Path("static")

def generate_weekly_poster(week):
    colors = json.load(open(STATIC_FOLDER / "colors.json"))
    
    img = Image.new('RGB', (800, 1100), color=(255, 255, 255))  # Tall poster
    draw = ImageDraw.Draw(img)
    font_title = ImageFont.truetype("arial.ttf", 28) if Path("arial.ttf").exists() else ImageFont.load_default()
    font_text = ImageFont.truetype("arial.ttf", 18) if Path("arial.ttf").exists() else ImageFont.load_default()
    font_activity = ImageFont.truetype("arial.ttf", 14) if Path("arial.ttf").exists() else ImageFont.load_default()

    draw.text((20, 20), f"Weekly Learning Overview at Eastwood Elementary: {week}", fill=colors["title"], font=font_title)
    
    y = 80
    students = get_students()
    plans = get_plans(week=week)
    for student in students:
        draw.text((20, y), f"{student[1]}", fill=colors["text"], font=font_text)
        y += 30
        student_plans = [p for p in plans if p[2] == student[0]]
        for plan in student_plans:
            draw.text((40, y), f"{plan[3]}: {plan[4]} (Mastery: {plan[6]})", fill=colors["activity"], font=font_activity)
            y += 20
        y += 20
    
    # Add logo
    logo_path = STATIC_FOLDER / "logo.png"
    if logo_path.exists():
        logo = Image.open(logo_path).resize((150, 150))
        img.paste(logo, (600, 900))

    poster_file = POSTER_FOLDER / f"weekly_poster_{week}.png"
    img.save(poster_file)
    return poster_file