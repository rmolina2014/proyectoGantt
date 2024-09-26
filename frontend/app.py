import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

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

    if not tasks:
        st.warning("No tasks available. Please create some tasks first.")
        return

    df = pd.DataFrame(tasks)
    df["project"] = df["project_id"].map({p["id"]: p["name"] for p in projects})
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])

    # Calculate the overall date range
    min_date = df["start_date"].min()
    max_date = df["end_date"].max()
    date_range = [min_date + timedelta(days=x) for x in range((max_date - min_date).days + 1)]

    # Create a custom color palette
    colors = px.colors.qualitative.Pastel

    fig = px.timeline(df, x_start="start_date", x_end="end_date", y="name", color="project",
                      title="Project Gantt Chart", labels={"name": "Task", "project": "Project"},
                      color_discrete_sequence=colors)

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=date_range,
            ticktext=[d.strftime('%d') for d in date_range],
            tickangle=0,
            tickfont=dict(size=10),
            title="Day of Month"
        ),
        yaxis=dict(title="Tasks"),
        height=400,
        title_x=0.5,
        legend_title_text="Projects",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Remove weekends
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"])
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

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