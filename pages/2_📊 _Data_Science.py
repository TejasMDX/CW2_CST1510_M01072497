import streamlit as st
from app.data.db import connect_database
from app.data.datasets import get_all_metadata,update_dataset_rows,delete_dataset,insert_dataset, get_dataset_by_uploader_count
from time import sleep

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

conn = connect_database('DATA/intelligence_platform.db')

st.title("Datasets Metadata Dashboard")

st.header("All Datasets Metadata ")
metadata = get_all_metadata(conn)
st.dataframe(metadata, use_container_width= True)

st.header("Datasets Metadata Counts by Uploader")
dataset_uploader_count =  get_dataset_by_uploader_count(conn)
st.bar_chart(dataset_uploader_count,x = "uploaded_by",y="count")

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