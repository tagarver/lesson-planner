import matplotlib.pyplot as plt
from db import get_plans, get_students
from pathlib import Path
import json

POSTER_FOLDER = Path("posters")
POSTER_FOLDER.mkdir(exist_ok=True)
STATIC_FOLDER = Path("static")

def generate_weekly_poster(week):
    # Load color palette
    colors = json.load(open(STATIC_FOLDER / "colors.json"))

    students = get_students()
    plans = get_plans(week=week)
    
    fig, ax = plt.subplots(figsize=(16,11))  # 11x17 poster
    ax.axis("off")
    ax.set_title(f"Weekly Learning Overview: {week}", fontsize=28, color=colors.get("title","black"))

    y = 1.0
    for student in students:
        ax.text(0.05, y, f"{student[1]}", fontsize=18, color=colors.get("text","black"), transform=fig.transFigure)
        student_plans = [p for p in plans if p[2]==student[0]]
        for plan in student_plans:
            y -= 0.03
            ax.text(0.1, y, f"{plan[3]}: {plan[4]}", fontsize=14, color=colors.get("activity","black"), transform=fig.transFigure)
        y -= 0.05
    poster_file = POSTER_FOLDER / f"weekly_poster_{week}.png"
    plt.savefig(poster_file, bbox_inches='tight')
    return poster_file
