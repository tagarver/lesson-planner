# poster.py (updated with better error handling)
from PIL import Image, ImageDraw, ImageFont
from db import get_plans, get_students
from pathlib import Path
import json

POSTER_FOLDER = Path("posters")
POSTER_FOLDER.mkdir(exist_ok=True)
STATIC_FOLDER = Path("static")

def generate_weekly_poster(week):
    # Default colors if JSON loading fails
    default_colors = {
        "title": "#002366",
        "text": "#000000", 
        "activity": "#CC0000",
        "background": "#FFFFFF",
        "header": "#4682B4",
        "accent": "#FFD700"
    }
    
    colors = default_colors  # Default to fallback colors
    
    # Try to load colors from JSON, fall back to defaults if error
    try:
        colors_path = STATIC_FOLDER / "colors.json"
        if colors_path.exists():
            colors = json.load(open(colors_path))
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Use default colors if there's an error
    
    img = Image.new('RGB', (800, 1100), color=colors.get("background", "#FFFFFF"))
    draw = ImageDraw.Draw(img)
    
    # ... rest of the function remains the same ...
    
    # Try to load a larger font if available
    try:
        font_title = ImageFont.truetype("arial.ttf", 20)
        font_text = ImageFont.truetype("arial.ttf", 14)
        font_activity = ImageFont.truetype("arial.ttf", 12)
    except:
        # Fall back to default fonts if arial.ttf is not available
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_activity = ImageFont.load_default()

    # Title
    draw.text((20, 20), f"Weekly Learning Overview at Eastwood Elementary: {week}", 
              fill=colors.get("title", "#000000"), font=font_title)
    
    y = 80
    students = get_students()
    plans = get_plans(week=week)
    
    for student in students:
        draw.text((20, y), f"{student[1]}'s Week:", 
                  fill=colors.get("text", "#000000"), font=font_text)
        y += 30
        
        student_plans = [p for p in plans if p[2] == student[0]]
        for plan in student_plans:
            # Safely extract the activity description
            activity_desc = plan[5]
            if "Objectives:" in activity_desc:
                try:
                    objective_line = activity_desc.split("Objectives: ")[1].split("\n")[0]
                except:
                    objective_line = plan[4]  # Fall back to lesson ID if parsing fails
            else:
                objective_line = plan[4]  # Fall back to lesson ID
                
            draw.text((40, y), f"{plan[3]}: {plan[4]} - {objective_line} (Mastery: {plan[6]})", 
                      fill=colors.get("activity", "#000000"), font=font_activity)
            y += 20
        y += 20
    
    # Add logo if available
    logo_path = STATIC_FOLDER / "logo.png"
    if logo_path.exists():
        try:
            logo = Image.open(logo_path).resize((150, 150))
            img.paste(logo, (600, 900))
        except:
            pass  # Skip logo if there's an error loading it

    poster_file = POSTER_FOLDER / f"weekly_poster_{week.replace(' ', '_')}.png"
    img.save(poster_file)
    return poster_file
