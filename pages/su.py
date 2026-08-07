import streamlit as st
import json
import csv
import uuid

login = open("login.json", "r")
data = json.load(login)

st.title("Students' Union Financial Dashboard")

add, delete, view = st.tabs(["Add Record", "Delete Record", "View Records"])

with add:
    with st.form("inputRecord"):
        club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")
        name = st.text_input("Item Name:")
        expenseType = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
        amount = st.number_input("Amount ($):", min_value=0.0)
        date = st.date_input("Date:")
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

with delete:
    pass

with view:
    with open('records.csv', 'r', newline="") as file:
        pass

leave = st.button("Logout")
if leave:
    st.switch_page("app.py")