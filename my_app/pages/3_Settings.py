import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
if not st.session_state.logged_in:
    st.error("You must be logged in to view this page")
    if st.button("Go to login"):
        st.switch_page("Home.py")
    st.stop()

st.title("⚙️Settings")

st.header("User Info")
with st.container():
    user = st.session_state.user
    st.write(f"Username: {user.get_username()}")
    st.write(f"Role: {user.get_role()}")

if st.button("Logout"):
    st.session_state.username = ""
    st.session_state.logged_in = False
    st.switch_page("Home.py")

 