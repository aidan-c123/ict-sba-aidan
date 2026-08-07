import streamlit as st
import json
import csv
import uuid

login = open("login.json", "r")
data = json.load(login)

st.title("Students' Union Financial Dashboard")

add, view = st.tabs(["Add Record", "View Records"])

with add:
    with st.form("inputRecord"):
        club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")
        name = st.text_input("Item Name:")
        amount = st.number_input("Amount ($):")
        date = st.date_input("Date:")
        expenseType = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
        submit = st.form_submit_button("Submit")

if submit:
    with open('records.csv', 'a', newline="") as file:
        writer = csv.writer(file)
        record_id = str(uuid.uuid4())
        if expenseType == "Income":
            writer.writerow([record_id, club, name, amount, date, expenseType])
        else:
            writer.writerow([record_id, club, name, -amount, date, expenseType])
    st.success("Submitted!")

with view:


back = st.button("Logout")
if back:
    st.switch_page("app.py")