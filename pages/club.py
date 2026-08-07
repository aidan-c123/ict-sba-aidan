import streamlit as st

f = open("id.txt", "r")
info = f.readlines()
f.close()
club = info[0].strip()

st.title(f"{club} Financial Dashboard")

back = st.button("Exit to Login")

if back:
    st.switch_page("app.py")