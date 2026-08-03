import streamlit as st

st.title("Club Financial Report")
with st.form("Login"):
    role = st.selectbox("What is your role?", ("Club Financial Secretary", "Student's Union"))
    if role == "Club Financial Secretary":
        club = st.selectbox("What is your club?", ("Music Society", "Civic Club"))
    st.form_submit_button('Submit')

