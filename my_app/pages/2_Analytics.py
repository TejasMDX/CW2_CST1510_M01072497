import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_incident_types_with_many_cases,get_high_severity_by_status, get_incidents_by_type_count
from app.data.tickets import get_tickets_by_assigned_to_count,get_high_piority_by_status,get_assigned_to_with_many_cases
from app.data.datasets import get_dataset_by_uploader_count
from time import sleep

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()


st.title("📊Analytics")

conn = connect_database('DATA/intelligence_platform.db')
incidents_tab, tickets_tab, datasets_tab = st.tabs(["Incidents", "IT Tickets", "Datasets Metadata"])

with incidents_tab:

    st.header("Incident Counts by Type")
    incident_type_count =  get_incidents_by_type_count(conn)
    st.bar_chart(incident_type_count, x="category", y="count")

    st.header("High-Severity Incidents by Status")
    high_severity = get_high_severity_by_status(conn)
    st.bar_chart(high_severity, x="status", y="count")
    

    st.header("Incident Types with Minimum Cases")
    min_count = st.text_input("Minimum count","5",key="min_count_incident_types")
    many_cases = get_incident_types_with_many_cases(conn,int(min_count))
    st.bar_chart(many_cases, x="category", y="count")

with tickets_tab:

    st.subheader("Ticket Counts by Assigned to")
    ticket_count_by_assigned_to = get_tickets_by_assigned_to_count(conn)
    st.bar_chart(ticket_count_by_assigned_to, x="assigned_to", y="count" )

    st.subheader("High Priority by Status")
    high_priority_by_status = get_high_piority_by_status(conn)
    st.bar_chart( high_priority_by_status,x="status", y="count")

    st.header("Assigned To with Minimum Cases")
    min_count = st.text_input("Minimum count","5", key="min_count_assigned_to")
    many_cases = get_assigned_to_with_many_cases(conn,int(min_count))
    st.bar_chart(many_cases, x="assigned_to", y="count" )

with datasets_tab:
    st.header("Datasets Metadata Counts by Uploader")
    dataset_uploader_count =  get_dataset_by_uploader_count(conn)
    st.bar_chart(dataset_uploader_count,x = "uploaded_by",y="count")

