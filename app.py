import streamlit as st
import pandas as pd
from db import init_db, add_student, get_students, save_plan
from pdf_generator import generate_student_pdf
from poster import generate_weekly_poster
from pathlib import Path

# Init DB
init_db()

st.title("Special Education Lesson Planner")

# Sidebar
week = st.sidebar.text_input("Week (e.g., Sep 1-5)", "")
student_name = st.sidebar.text_input("New Student Name", "")
accommodations = st.sidebar.text_area("Accommodations", "")
iep_link = st.sidebar.text_input("IEP Link", "")

if st.sidebar.button("Add Student") and student_name:
    add_student(student_name, accommodations, iep_link)
    st.sidebar.success(f"Added {student_name}")

students = get_students()
student_options = {s[1]: s[0] for s in students}

selected_student = st.selectbox("Select Student", list(student_options.keys()))

# Load mappings
uls_mapping = pd.read_csv("mappings/uls.csv")
wilson_mapping = pd.read_csv("mappings/wilson.csv")

st.subheader("Create Lesson Plan")

lesson_id = st.selectbox("Select Lesson (ULS or Wilson ID)", uls_mapping['Lesson_ID'].tolist() + wilson_mapping['Lesson_ID'].tolist())
activity = st.text_area("Activity", "")

mastery = st.selectbox("Mastery Level", ["Not Started", "In Progress", "Mastered"])

if st.button("Save Plan"):
    save_plan(week, student_options[selected_student], lesson_id, activity, mastery)
    st.success("Plan saved!")

if st.button("Generate Student PDF"):
    pdf_file = generate_student_pdf(student_options[selected_student], week)
    st.success(f"PDF generated: {pdf_file}")
    st.download_button("Download PDF", data=open(pdf_file, "rb").read(), file_name=pdf_file.name)

if st.button("Generate Weekly Poster"):
    poster_file = generate_weekly_poster(week)
    st.success(f"Poster generated: {poster_file}")
    st.image(poster_file)
