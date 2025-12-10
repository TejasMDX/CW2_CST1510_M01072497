import streamlit as st
from app.data.db import connect_database
from app.data.tickets import get_all_tickets,insert_ticket,delete_ticket,update_ticket_status,get_tickets_by_assigned_to_count,get_high_piority_by_status,get_assigned_to_with_many_cases
from time import sleep

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

conn = connect_database('DATA/intelligence_platform.db')

st.title("IT Tickets Dashboard")

st.header("All IT Tickets")
tickets = get_all_tickets(conn)

st.dataframe(tickets, use_container_width= True)

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