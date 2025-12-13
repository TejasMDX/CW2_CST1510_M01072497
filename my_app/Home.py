import streamlit as st

from app.data.users import get_user_by_username, insert_user
from auth import verify_password,check_password_strength,validate_username,validate_password, hash_password
from time import sleep
from models.user import User

st.title("🏠Home")

# Initialize session state variables if not already set
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# If the user is already logged in, show dashboard access
if st.session_state.logged_in:
    user = st.session_state.user
    st.success(f"Logged in as **{user.get_username()}** (role: {user.get_role()}).")


    st.subheader("View Dashboard")
    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")   
    st.stop() # Stop further execution for logged-in users

# Create login and register tabs
tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:

    st.subheader("Login")

    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Log in", type="primary"):
        user_data = get_user_by_username(username)

        if not user_data:
            st.error("❌ Username not found.")
        
        else:
            user_id, db_username, db_hash, role, created = user_data

            # Check if password is correct
            if verify_password(password, db_hash):

                user_obj = User(username=db_username, password_hash=db_hash, role=role)

                # Login successful: save info in session state
                st.session_state.logged_in = True
                st.session_state.user = user_obj

                st.success(f"Welcome back, {db_username}! 🎉")
                sleep(2)
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

with tab_register:
    st.subheader("Register")

    new_username = st.text_input("Choose a username", key="register_username")
    new_password = st.text_input("Choose a password", type="password", key="register_password")

    # Show password strength
    if new_password:
        strength = check_password_strength(new_password)
        st.info(f"Password Strength: {strength}")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm")

    if st.button("Create account"):
        # Validate username
        valid, message = validate_username(new_username)
        if not valid:
            st.error(message)
            st.stop()
        
        # Validate password
        valid_pw, message = validate_password(new_password)
        if not valid_pw:
            st.error(message)
            st.stop()
        
        # Check password confirmation
        if new_password != confirm_password:
            st.error("Passwords do not match")
            st.stop()

        # Check if username already exists
        if get_user_by_username(new_username):
            st.error("Username already exists")
            st.stop()

        # Hash the password and insert the new user
        hashed_pw = hash_password(new_password)

        insert_user(new_username, hashed_pw)

        st.success("Account created! You can now log in from the Login tab.")
        st.info("Tip: go to the Login tab and sign in with your new account.")