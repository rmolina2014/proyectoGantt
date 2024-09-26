import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_URL = "http://localhost:8000"

def create_project():
    st.subheader("Create Project")
    name = st.text_input("Project Name")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Create Project"):
        response = requests.post(f"{API_URL}/projects/", json={
            "name": name,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        if response.status_code == 200:
            st.success("Project created successfully!")
        else:
            st.error("Failed to create project")

def create_task():
    st.subheader("Create Task")
    projects = requests.get(f"{API_URL}/projects/").json()
    project_names = [project["name"] for project in projects]
    project_name = st.selectbox("Select Project", project_names)
    project_id = next(project["id"] for project in projects if project["name"] == project_name)
    name = st.text_input("Task Name")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Create Task"):
        response = requests.post(f"{API_URL}/tasks/", json={
            "project_id": project_id,
            "name": name,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        })
        if response.status_code == 200:
            st.success("Task created successfully!")
        else:
            st.error("Failed to create task")

def display_gantt_chart():
    st.subheader("Gantt Chart")
    projects = requests.get(f"{API_URL}/projects/").json()
    tasks = requests.get(f"{API_URL}/tasks/").json()

    df = pd.DataFrame(tasks)
    df["project"] = df["project_id"].map({p["id"]: p["name"] for p in projects})
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    fig = px.timeline(df, x_start="start_date", x_end="end_date", y="project", color="name",
                      title="Project Gantt Chart", labels={"name": "Task"})
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)

def main():
    st.title("Project Management App")

    menu = ["Create Project", "Create Task", "View Gantt Chart"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Project":
        create_project()
    elif choice == "Create Task":
        create_task()
    elif choice == "View Gantt Chart":
        display_gantt_chart()

if __name__ == "__main__":
    main()