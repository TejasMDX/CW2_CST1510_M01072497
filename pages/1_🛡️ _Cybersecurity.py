import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident, delete_incident, update_incident_status,get_high_severity_by_status,get_incident_types_with_many_cases,get_incidents_by_type_count
from time import sleep

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

conn = connect_database('DATA/intelligence_platform.db')

st.title("Cyber Incidents Dashboard")

st.header("All incidents")
incidents = get_all_incidents(conn)

st.dataframe(incidents, use_container_width= True)

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

st.header("Incident Operations")
operation = st.selectbox("Operation",["Add Incident","Update Incident Status","Delete Incident"])

match operation:
    case "Add Incident":
        #CREATE: Add new incident with a form 
        with st.form("new_incident"):
            #form inputs
            date = st.date_input("Date")
            title = st.text_input("Incident Title")
            description = st.text_input("Desciption")
            severity = st.selectbox("Severity",["Low","Medium","High","Critical"])
            status = st.selectbox("Satus",["Open","In Progress", "Resolved"])
            reported_by = st.text_input("Reported by")

            #submit form button
            submitted =st.form_submit_button("Add Incident")

        #when form is submitted
        if submitted and title:
            #call week8 function itno database
            insert_incident(conn,date,title,severity,status,description,reported_by)
            st.success("√ Incident added successfully!")
            sleep(2)
            st.rerun()
        
    case "Update Incident Status":
        with st.form("update_incident_status"):
            incident_id = st.text_input("Incident ID")
            new_status = st.selectbox("Status",["Open","In Progress", "Resolved"])

            submitted = st.form_submit_button("Update Incident Status")

        if submitted and incident_id and new_status:
                
            update_incident_status(conn,incident_id,new_status)
            st.success("√ Status of incident was updated successfully!")
            sleep(2)
            st.rerun()
        
    case "Delete Incident":
        with st.form("delete_incident"):
            incident_id = st.text_input("Incident ID")

            submitted = st.form_submit_button("Delete Incident")

        if submitted and incident_id:
                
            delete_incident(conn,incident_id)
            st.success("√ Incident deleted successfully!")
            sleep(2)
            st.rerun()