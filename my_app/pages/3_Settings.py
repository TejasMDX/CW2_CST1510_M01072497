import streamlit as st

if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️Settings")

st.header("User Info")
with st.container():
    st.write(f"Username: {st.session_state.username}")
    st.write(f"Role: {st.session_state.role}")

if st.button("Logout"):
    st.session_state.username = ""
    st.session_state.logged_in = False
    st.switch_page("Home.py")

 