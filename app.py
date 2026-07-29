import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("AI Attendance System")

# Register student
st.sidebar.header("Register Student")
name = st.sidebar.text_input("Student Name")
uploaded_image = st.sidebar.file_uploader("Upload Photo", type=["jpg", "jpeg", "png"])

if uploaded_image and name:
    if not os.path.exists("students"):
        os.makedirs("students")
    with open(f"students/{name}.jpg", "wb") as f:
        f.write(uploaded_image.getvalue())
    st.sidebar.success(f"Registered: {name}")

# Mark attendance
st.header("Mark Attendance")
student_name = st.text_input("Enter Student Name")

if st.button("Mark Present") and student_name:
    if not os.path.exists("attendance.csv"):
        df = pd.DataFrame(columns=["Name", "Time", "Status"])
        df.to_csv("attendance.csv", index=False)
    
    df = pd.read_csv("attendance.csv")
    new_row = pd.DataFrame({
        "Name": [student_name], 
        "Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], 
        "Status": ["Present"]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("attendance.csv", index=False)
    st.success(f"Marked present: {student_name}")

# Show attendance
if os.path.exists("attendance.csv"):
    st.header("Attendance Record")
    df = pd.read_csv("attendance.csv")
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "attendance.csv")