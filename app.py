import streamlit as st
import json

st.title("Club Financial Report")

st.set_page_config(page_title="SJC Club Financial Management System", page_icon=None, initial_sidebar_state="collapsed")

f = open("id.txt", "w")
club = ""
login = open("login.json", "r")
data = json.load(login)


club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")

pwd = st.text_input("Password:", type="password")


submit = st.button("Login")

if submit:
    f.write(club)

    if pwd == data[club]:
        st.success("Login successful")

        if club != "Students' Union":
            st.switch_page("pages/club.py")

        else:
            st.switch_page("pages/admin.py")

    else:
        st.error("Incorrect password")

f.close()