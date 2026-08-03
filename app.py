import streamlit as st
import json

st.title("Club Financial Report")

st.set_page_config(page_title="SJC Club Financial Management System", page_icon=None, initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

f = open("id.txt", "w")
club = ""
login = open("login.json", "r")
data = json.load(login)

role = st.selectbox("What is your role?", ("Club Financial Secretary", "Students' Union"), index=None, placeholder = "Select role...")

if role == "Club Financial Secretary":
    club = st.selectbox("What is your club?", ("Music Society", "Civic Club"), index=None, placeholder="Select club...")



submit = st.button("Login")

if submit:
    f.write(role + "\n")
    f.write(club)
    if role == "Club Financial Secretary":
        st.switch_page("pages/club.py")
    else:
        st.switch_page("pages/su.py")