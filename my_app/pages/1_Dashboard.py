import streamlit as st
from app.data.db import connect_database
from app.data.incidents import get_all_incidents, insert_incident, delete_incident, update_incident_status
from app.data.tickets import get_all_tickets,insert_ticket,delete_ticket,update_ticket_status
from app.data.datasets import get_all_metadata,update_dataset_rows,delete_dataset,insert_dataset
from time import sleep

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("📊Dashboard")
st.success(f"Welcome,{st.session_state.username}!")

conn = connect_database('DATA/intelligence_platform.db')

incidents_tab, tickets_tab, datasets_tab = st.tabs(["Incidents", "IT Tickets", "Datasets Metadata"])

with incidents_tab:
    st.header("All incidents")
    incidents = get_all_incidents(conn)
    st.dataframe(incidents, use_container_width= True)

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

with tickets_tab:
    st.header("All IT Tickets")
    tickets = get_all_tickets(conn)
    st.dataframe(tickets, use_container_width= True)

    st.header("IT Ticket Operations")
    operation = st.selectbox("Operation",["Add Ticket","Update Ticket Status","Delete Ticket"])

    match operation:
        case "Add Ticket":
            with st.form("new_ticket"):
                priority = st.selectbox("Priority",["Low","Medium","High","Critical"])
                description = st.text_input("Desciption")
                status = status = st.selectbox("Satus",["Open","In Progress", "Resolved","Waiting for User"])
                resolution_time_hours = st.number_input("Resolution time in hours", step=1)
                assigned_to = st.text_input("Assinged to")
                
                submitted =st.form_submit_button("Add Ticket")

            if submitted:
                insert_ticket(conn,priority,description,status,assigned_to,resolution_time_hours)
                st.success("√ IT Ticket added successfully!")
                sleep(2)
                st.rerun()
    
        case "Update Ticket Status":
            with st.form("update_ticket_status"):
                ticket_id = st.text_input("IT Ticket ID")
                new_status = st.selectbox("Status",["Open","In Progress", "Resolved","Waiting for User"])

                submitted = st.form_submit_button("Update IT Ticket Status")

            if submitted:
                update_ticket_status(conn,ticket_id,new_status)
                st.success("√ Status of IT Ticket was updated successfully!")
                sleep(2)
                st.rerun()

        case "Delete Ticket":
            with st.form("delete_ticket"):
                ticket_id = st.text_input("IT Ticket ID")

                submitted = st.form_submit_button("Delete IT Ticket Status")

            if submitted and ticket_id:
                delete_ticket(conn,ticket_id)
                st.success("√ IT Ticket deleted successfully!")
                sleep(2)
                st.rerun()

with datasets_tab:
    st.header("All Datasets Metadata ")
    metadata = get_all_metadata(conn)
    st.dataframe(metadata, use_container_width= True)

    st.header("Datasets Metadata Operations")
    operation = st.selectbox("Operation",["Add Dataset","Update Dataset","Delete Dataset"])

    match operation:
        case "Add Dataset":
            with st.form("new_dataset"):

                name = st.text_input("Name")
                rows = st.number_input("Number of Rows", step=1)
                columns = st.number_input("Number of Columns", step=1)
                upload_by = st.text_input("Upload by")
                upload_date = st.date_input("Upload Date")
                
                submitted =st.form_submit_button("Add Dataset")

            if submitted:
                insert_dataset(conn,name,rows,columns,upload_by,upload_date)
                st.success("√ Dataset added successfully!")
                sleep(2)
                st.rerun()

        case "Update Dataset":
            with st.form("update_dataset"):

                dataset_id = st.text_input("Dataset ID")
                new_rows = st.number_input("Number of Rows", step=1)

                submitted = st.form_submit_button("Update Dataset")

            if submitted:
                update_dataset_rows(conn,dataset_id,new_rows)
                st.success("√ Dataset updated successfully!")
                sleep(2)
                st.rerun()


        case "Delete Dataset":
            with st.form("delete_dataset"):
                dataset_id = st.text_input("Dataset ID")

                submitted = st.form_submit_button("Delete Dataset")

            if submitted and dataset_id:
                delete_dataset(conn,dataset_id)
                st.success("√ Dataset deleted successfully!")
                sleep(2)
                st.rerun()