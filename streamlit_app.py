import streamlit as st
from auth import init_db, authenticate

# Initialize the database
st.set_page_config(page_title="PF Hero", layout="centered")
init_db()

# Set session defaults
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None

ROLES = [None, "user", "admin"]

# --- Login function using real authentication ---
def login():
    st.header("Debate Helper Pro")
    st.subheader("Your personal Debate AI assistant")
    with st.form("login_form"):
        username = st.text_input("Username", key="input_username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            success, role = authenticate(username, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = role
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")

# --- Logout function ---
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.rerun()

# --- Get current role ---
role = st.session_state.get("role", None)

# --- Define Pages ---
# --- User Pages ---
get_writing = st.Page("pages_user/get_writing.py", title="Get Writing", icon="✍️", default=(role == "user"))
get_research = st.Page("pages_user/get_research.py", title="Get Research", icon="🔍")
get_feedback = st.Page("pages_user/get_feedback.py", title="Get Feedback", icon="📝")

# --- Admin Pages ---
manage_users = st.Page("pages_admin/manage_users.py", title="Manage Users", icon="👥", default=(role == "admin"))
add_users = st.Page("pages_admin/add_users.py", title="Add Users", icon="➕")
io_history = st.Page("pages_admin/io_history.py", title="I/O History", icon="📄")
usage_data = st.Page("pages_admin/usage_data.py", title="Usage Data", icon="📊")

# --- Account Pages ---
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings_page = st.Page("pages_account/settings.py", title="Settings", icon=":material/settings:")

account_pages = [logout_page, settings_page]

# --- Organize pages based on role ---
page_dict = {}

if not st.session_state.authenticated:
    # Only login page if not authenticated
    pg = st.navigation([st.Page(login)])
else:
    # Authenticated pages
    if role == "user":
        page_dict["Use the App"] = [get_writing, get_research, get_feedback]
    if role == "admin":
        page_dict["Admin"] = [manage_users, add_users, io_history, usage_data]
        page_dict["User Services"] = [get_writing, get_research, get_feedback]
    pg = st.navigation({"Account": account_pages} | page_dict)

# Run the navigation
pg.run()