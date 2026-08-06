import streamlit as st

f = open("id.txt", "r")
info = f.readlines()
st.title(f"{info[0].strip()} Financial Dashboard")

back = st.button("Exit to Login")

if back:
    st.switch_page("app.py")