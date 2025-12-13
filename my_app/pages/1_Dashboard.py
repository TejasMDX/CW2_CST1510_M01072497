import streamlit as st
from app.data.db import connect_database
from services.database_manager import DatabaseManager
from models.security_incident import SecurityIncident
from models.dataset import Dataset
from models.it_ticket import ITTicket
from app.data.incidents import get_all_incidents, insert_incident, delete_incident, update_incident_status
from app.data.tickets import get_all_tickets,insert_ticket,delete_ticket,update_ticket_status
from app.data.datasets import get_all_metadata,update_dataset_rows,delete_dataset,insert_dataset
from time import sleep


#check if user is login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

#for database connection
db =DatabaseManager("DATA/intelligence_platform.db")
db.connect()

st.title("📊Dashboard")
user = st.session_state.user
st.success(f"Welcome, {user.get_username()}!")

## Fetch all records
conn = connect_database('DATA/intelligence_platform.db')
incidents_rows = get_all_incidents(db)
tickets_rows = get_all_tickets(db)
metadata_rows = get_all_metadata(db)

db.close()

# Create Tabs for different sections
incidents_tab, tickets_tab, datasets_tab = st.tabs(["Incidents", "IT Tickets", "Datasets Metadata"])

# INCIDENTS TAB
with incidents_tab:
    st.header("All incidents")
    st.write(incidents_rows)  # Display all incidents

    st.header("Incident Operations")
    operation = st.selectbox("Operation",["Add Incident","Update Incident Status","Delete Incident"])

     # Handle different operations
    match operation:
        case "Add Incident":
            #Add new incident with a form 
            with st.form("new_incident"):
                #form inputs
    
                category = st.text_input("Incident Category")
                description = st.text_input("Desciption")
                severity = st.selectbox("Severity",["Low","Medium","High","Critical"])
                status = st.selectbox("Satus",["Open","In Progress", "Resolved"])
                reported_by = st.text_input("Reported by")


                #submit form button
                submitted =st.form_submit_button("Add Incident")


            # Insert incident into database
            if submitted:
                if category and description and severity and status:
              
                    incident = SecurityIncident(category=category,severity=severity,status=status,description=description,reported_by=reported_by)

                    insert_incident(conn,incident.get_category(),incident.get_severity(),incident.get_status(),incident.get_description(),incident.get_reported_by())
                    st.success("√ Incident added successfully!")
                    sleep(2)
                    st.rerun() # Refresh page to show updated data
                else:
                    st.error("❌Please fill in all required fields: Category, Description, Severity, and Status")
                
        
        case "Update Incident Status":
            # Update incident status form
            with st.form("update_incident_status"):
                incident_id = st.text_input("Incident ID")
                new_status = st.selectbox("Status",["Open","In Progress", "Resolved"])


                submitted = st.form_submit_button("Update Incident Status")

            # Update status in database
            if submitted and incident_id and new_status:
                
                db =DatabaseManager("DATA/intelligence_platform.db")
                db.connect()


                row = db.fetch_one("SELECT incident_id, category, severity, status, description, timestamp, reported_by "
        "FROM cyber_incidents WHERE incident_id=?",
        (incident_id,))
                
                if row:
            
                    incident = SecurityIncident(
                        incident_id=row[0],
                        category=row[1],
                        severity=row[2],
                        status=row[3],
                        description=row[4],
                        timestamp=row[5],
                        reported_by=row[6]
                    )

                    incident.update_status(new_status)

                    update_incident_status(conn, incident.get_id(),incident.get_status())
    
                    db.close()

                    st.success("√ Status of incident was updated successfully!")
                    
                else:
                    st.error("❌ Incident ID not found. Please check and try again.")
                sleep(2)
                st.rerun()

            
        
        case "Delete Incident":
            # Delete incident form
            with st.form("delete_incident"):
                incident_id = st.text_input("Incident ID")

                submitted = st.form_submit_button("Delete Incident")

            if submitted and incident_id:
                
                db =DatabaseManager("DATA/intelligence_platform.db")
                db.connect()

                row = db.fetch_one("SELECT incident_id, category, severity, status, description, timestamp, reported_by "
            "FROM cyber_incidents WHERE incident_id=?",
            (incident_id,))
                    
                if row:
                
                    incident = SecurityIncident(
                        incident_id=row[0],
                        category=row[1],
                        severity=row[2],
                        status=row[3],
                        description=row[4],
                        timestamp=row[5],
                        reported_by=row[6]
                        )
                    
                    delete_incident(conn,incident.get_id())
                    st.success("√ Incident deleted successfully!")
                else:
                    st.error("❌ Incident ID not found. Please check and try again.")
            
                sleep(2)
                st.rerun()

# IT TICKETS TAB
with tickets_tab:
    st.header("All IT Tickets")
    st.write(tickets_rows) # Display all IT tickets

    st.header("IT Ticket Operations")
    operation = st.selectbox("Operation",["Add Ticket","Update Ticket Status","Delete Ticket"])

    match operation:
        case "Add Ticket":
             # Add new IT ticket
            with st.form("new_ticket"):
                priority = st.selectbox("Priority",["Low","Medium","High","Critical"])
                description = st.text_input("Desciption")
                status = status = st.selectbox("Satus",["Open","In Progress", "Resolved","Waiting for User"])
                resolution_time_hours = st.number_input("Resolution time in hours", step=1)
                assigned_to = st.text_input("Assinged to")
                
                submitted =st.form_submit_button("Add Ticket")

            if submitted:
                if resolution_time_hours < 1:
                    st.error("❌ Resolution time in hours must be a greater than 0!")
                elif description and resolution_time_hours and resolution_time_hours and assigned_to:
                    ticket = ITTicket(
                        ticket_id=0,        
                        priority=priority,
                        description=description,
                        status=status,
                        assigned_to=assigned_to,
                        created_at="",               
                        resolution_time_hours=resolution_time_hours
                    )

                    insert_ticket(conn,ticket.priority,ticket.description,ticket.status,ticket.assigned_to,ticket.resolution_time_hours)

                    st.success("√ IT Ticket added successfully!")
                else:
                    st.error("❌ Please enter all the fields")
                sleep(2)
                st.rerun()
    
        case "Update Ticket Status":
            # Update IT ticket status
            with st.form("update_ticket_status"):
                ticket_id = st.text_input("IT Ticket ID")
                new_status = st.selectbox("Status",["Open","In Progress", "Resolved","Waiting for User"])

                submitted = st.form_submit_button("Update IT Ticket Status")

            if submitted:
                db = DatabaseManager("DATA/intelligence_platform.db")
                db.connect()

                row = db.fetch_one(
                        "SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours "
                        "FROM it_tickets WHERE ticket_id=?",
                        (ticket_id,))
                
                
                if row:
                    ticket = ITTicket(
                        ticket_id=row[0],
                        priority=row[1],
                        description=row[2],
                        status=row[3],
                        assigned_to=row[4],
                        created_at=row[5],
                        resolution_time_hours=row[6]
                    )

                    ticket.status = new_status
                    update_ticket_status(conn, ticket.ticket_id, ticket.status)

                    st.success("√ Status of IT Ticket was updated successfully!")
                    db.close()
                else:
                    st.error("❌ Ticket ID not found. Please check and try again.")
                sleep(2)
                st.rerun()

        case "Delete Ticket":
            # Delete IT ticket
            with st.form("delete_ticket"):
                ticket_id = st.text_input("IT Ticket ID")

                submitted = st.form_submit_button("Delete IT Ticket Status")

            if submitted and ticket_id:

                db = DatabaseManager("DATA/intelligence_platform.db")
                db.connect()

                row = db.fetch_one(
                    "SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours "
                    "FROM it_tickets WHERE ticket_id=?",
                (ticket_id,))

                if row:
                    ticket = ITTicket(
                    ticket_id=row[0],
                    priority=row[1],
                    description=row[2],
                    status=row[3],
                    assigned_to=row[4],
                    created_at=row[5],
                    resolution_time_hours=row[6]
                )

                    delete_ticket(conn, ticket.ticket_id)
                    st.success("√ IT Ticket deleted successfully!")
                    db.close()
                else:
                    st.error("❌ Ticket ID not found. Please check and try again.")
                sleep(2)
                st.rerun()

# DATASETS TAB
with datasets_tab:
    st.header("All Datasets Metadata ")
    st.write(metadata_rows) # Display all dataset metadata

    st.header("Datasets Metadata Operations")
    operation = st.selectbox("Operation",["Add Dataset","Update Dataset","Delete Dataset"])

    match operation:
        case "Add Dataset":
            # Add new dataset
            with st.form("new_dataset"):

                name = st.text_input("Name")
                rows = st.number_input("Number of Rows", step=1)
                columns = st.number_input("Number of Columns", step=1)
                uploaded_by = st.text_input("Upload by")
                upload_date = st.date_input("Upload Date")
                
                submitted =st.form_submit_button("Add Dataset")

            if submitted:

                if rows < 0 or columns < 0 :
                    st.error("Number of rows and columns cannot be less than 0!")
                elif name and uploaded_by :

                    dataset = Dataset(
                        dataset_id=0,         
                        name=name,
                        rows=rows,
                        columns=columns,
                        uploaded_by=uploaded_by,
                        upload_date=str(upload_date)
                    )

                    insert_dataset(conn,dataset.name,dataset.rows,dataset.columns,dataset.uploaded_by,dataset.upload_date)

                    st.success("√ Dataset added successfully!")
                else:
                    st.error("❌ Please enter all the fields")
                sleep(2)
                st.rerun()

        case "Update Dataset":
            # Update dataset rows
            with st.form("update_dataset"):

                dataset_id = st.text_input("Dataset ID")
                new_rows = st.number_input("Number of Rows", step=1)

                submitted = st.form_submit_button("Update Dataset")
                

            if submitted:

                if new_rows < 0 :
                    st.error("❌ Number of rows cannot be negative!")
                else:
                    db = DatabaseManager("DATA/intelligence_platform.db")
                    db.connect()

                    row = db.fetch_one(
                        "SELECT dataset_id, name, rows, columns, uploaded_by, upload_date "
                        "FROM datasets_metadata WHERE dataset_id=?",
                        (dataset_id,))
                    
                    if row:
                        dataset = Dataset(
                        dataset_id=row[0],
                        name=row[1],
                        rows=row[2],
                        columns=row[3],
                        uploaded_by=row[4],
                        upload_date=row[5]
                    )
                        
                        dataset.rows = new_rows

                        update_dataset_rows(conn, dataset.dataset_id, dataset.rows)

                        st.success("√ Dataset updated successfully!")
                        db.close()
                    else:
                        st.error("❌ Dataset ID not found. Please check and try again.")
                sleep(2)
                st.rerun()


        case "Delete Dataset":
            # Delete dataset form
            with st.form("delete_dataset"):
                dataset_id = st.text_input("Dataset ID")

                submitted = st.form_submit_button("Delete Dataset")

            if submitted and dataset_id:

                db = DatabaseManager("DATA/intelligence_platform.db")
                db.connect()

                row = db.fetch_one(
                    "SELECT dataset_id, name, rows, columns, uploaded_by, upload_date "
                    "FROM datasets_metadata WHERE dataset_id=?",
                    (dataset_id,))
                
                if row:
                    dataset = Dataset(
                        dataset_id=row[0],
                        name=row[1],
                        rows=row[2],
                        columns=row[3],
                        uploaded_by=row[4],
                        upload_date=row[5]
                    )

                    delete_dataset(conn, dataset.dataset_id)
                    st.success("√ Dataset deleted successfully!")
                    db.close()
                else:
                    st.error("❌ Dataset ID not found. Please check and try again.")
                sleep(2)
                st.rerun()