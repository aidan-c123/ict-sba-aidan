import streamlit as st

st.title("Student's Union Financial Dashboard")

back = st.button("Exit to Login")

if back:
    st.switch_page("app.py")