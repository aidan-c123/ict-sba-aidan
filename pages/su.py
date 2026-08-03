import streamlit as st

st.title("Students' Union Financial Dashboard")

back = st.button("Exit to Login")

if back:
    st.switch_page("app.py")