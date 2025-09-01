import streamlit as st
import pandas as pd
from db import init_db, add_student, get_students, save_plan, get_plans, get_next_lesson
from pdf_generator import generate_student_pdf
from poster import generate_weekly_poster
from pathlib import Path
from datetime import datetime, timedelta

# Init DB
init_db()

st.title("Eastwood Special Ed Planning App - Automated Edition")

# Sidebar for student management
st.sidebar.header("Student Management")
student_name = st.sidebar.text_input("New Student Name", "")
accommodations = st.sidebar.text_area("Accommodations", "")
iep_link = st.sidebar.text_input("IEP Link", "")

if st.sidebar.button("Add Student") and student_name:
    add_student(student_name, accommodations, iep_link)
    st.sidebar.success(f"Added {student_name}")

students = get_students()
student_options = {s[1]: s[0] for s in students}
selected_student = st.selectbox("Select Student", list(student_options.keys()))
student_id = student_options[selected_student]

# Load mappings
uls_df = pd.read_csv("mappings/uls.csv")
math_df = pd.read_csv("mappings/math.csv")
life_df = pd.read_csv("mappings/life_skills.csv")

# Auto week based on current date (Sep 1, 2025)
today = datetime(2025, 9, 1)
week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=4)
week = f"{week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"

st.subheader(f"Auto-Generate Plans for Week: {week}")

subjects = ["Life Skills", "Literacy (ULS)", "Math (Coins/Expressions)"]

# Month-based ULS suggestion
month = today.month
uls_monthly = {9: "Back to School/Community", 10: "History and Change", 11: "Weather Wonders", 12: "Holiday Traditions"}  # Expanded from research
uls_theme = uls_monthly.get(month, "General Review")

for subject in subjects:
    df = {"Life Skills": life_df, "Literacy (ULS)": uls_df, "Math (Coins/Expressions)": math_df}[subject]
    next_lesson = get_next_lesson(student_id, subject, df)
    if subject == "Literacy (ULS)":
        st.write(f"Suggested next for {subject} (Theme: {uls_theme}): {next_lesson}")
    else:
        st.write(f"Suggested next for {subject}: {next_lesson}")
    lesson_id = st.selectbox(f"Select/Confirm {subject} Lesson", df['Lesson_ID'].tolist(), index=df[df['Lesson_ID']==next_lesson].index[0])
    
    row = df[df['Lesson_ID'] == lesson_id].iloc[0]
    detailed_plan = f"Objectives: {row['Objectives']}\nMaterials: {row['Materials']}\nSteps: {row['Steps']}\nAssessment: {row['Assessment']}\nStandard: {row['Standard']} - {row['Standard_Description']}"
    detailed_plan = st.text_area(f"{subject} Detailed Plan (Auto-Filled)", detailed_plan, height=250)
    
    mastery = st.selectbox(f"{subject} Mastery Level", ["Not Started", "In Progress", "Mastered"], index=1)

    if st.button(f"Save {subject} Plan"):
        save_plan(week, student_id, subject, lesson_id, detailed_plan, mastery)
        st.success(f"{subject} Plan saved!")

# One-click generate full week
if st.button("Auto-Generate & Save Full Week Plans"):
    for subject in subjects:
        df = {"Life Skills": life_df, "Literacy (ULS)": uls_df, "Math (Coins/Expressions)": math_df}[subject]
        next_lesson = get_next_lesson(student_id, subject, df)
        row = df[df['Lesson_ID'] == next_lesson].iloc[0]
        detailed_plan = f"Objectives: {row['Objectives']}\nMaterials: {row['Materials']}\nSteps: {row['Steps']}\nAssessment: {row['Assessment']}\nStandard: {row['Standard']} - {row['Standard_Description']}"
        save_plan(week, student_id, subject, next_lesson, detailed_plan, "In Progress")
    st.success("Full week plans auto-generated and saved!")

# Outputs
col1, col2 = st.columns(2)
with col1:
    if st.button("Generate Student PDF"):
        pdf_file = generate_student_pdf(student_id, week)
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF", f.read(), file_name=pdf_file.name)
with col2:
    if st.button("Generate Weekly Poster"):
        poster_file = generate_weekly_poster(week)
        st.image(str(poster_file))

# Historical
tab1, tab2 = st.tabs(["Historical Plans", "Mastery Tracking"])
with tab1:
    df_plans = pd.DataFrame(get_plans(), columns=["ID", "Week", "Student ID", "Subject", "Lesson ID", "Detailed Plan", "Mastery"])
    st.dataframe(df_plans)
with tab2:
    for subject in subjects:
        subj_plans = get_plans(student_id=student_id, subject=subject)
        st.subheader(subject)
        if subj_plans:
            st.dataframe(pd.DataFrame(subj_plans, columns=["ID", "Week", "Student ID", "Subject", "Lesson ID", "Detailed Plan", "Mastery"]))
        else:
            st.write("No plans yet.")