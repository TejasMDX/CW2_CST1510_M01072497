import streamlit as st

from app.data.users import get_user_by_username, insert_user
from auth import verify_password,check_password_strength,validate_username,validate_password, hash_password
from time import sleep

st.title("🏠 Home")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"

if st.session_state.logged_in:
    st.success(f"Logged in as **{st.session_state.username}**.")

    if st.button("Go to Cyber Incidents Dashboard"):
        st.switch_page("pages/1_🛡️ _Cybersecurity.py")   

    if st.button("Go to Datasets Metadata Dashboard"):
        st.switch_page("pages/2_📊 _Data_Science.py")   

    if st.button("Go to IT Tickets Dashboard"):
        st.switch_page("pages/3_💻 _IT_Operations.py")   
 
    if st.button("Go to AI_Assistant"):
        st.switch_page("pages/4_🤖 _AI_Assistant.py")    

    if st.button("Logout"):
        st.session_state.username = ""
        st.session_state.logged_in = False


    st.stop()



tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:

    st.subheader("Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log in", type="primary"):
        user = get_user_by_username(username)

        if not user:
            st.error("❌ Username not found.")
        
        else:
            user_id, db_username, db_hash, role, created = user

            if verify_password(password, db_hash):
                # SUCCESS LOGIN
                st.session_state.logged_in = True
                st.session_state.username = db_username
                st.session_state.role = role

                st.success(f"Welcome back, {db_username}! 🎉")
                sleep(2)
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")

    if new_password:
        strength = check_password_strength(new_password)
        st.info(f"Password Strength: {strength}")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        valid, message = validate_username(new_username)
        if not valid:
            st.error(message)
            st.stop()
        
        valid_pw, message = validate_password(new_password)
        if not valid_pw:
            st.error(message)
            st.stop()
        
        if new_password != confirm_password:
            st.error("Passwords do not match")
            st.stop()

        if get_user_by_username(new_username):
            st.error("Username already exists")
            st.stop()

        hashed_pw = hash_password(new_password)

        insert_user(new_username, hashed_pw)

        st.success("Account created! You can now log in from the Login tab.")
        st.info("Tip: go to the Login tab and sign in with your new account.")