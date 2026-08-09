import streamlit as st
import json
import csv
import uuid
import pandas as pd

login = open("login.json", "r")
data = json.load(login)
login.close()

st.title("Students' Union Financial Dashboard")

view, add, delete = st.tabs(["View Records", "Add Record", "Delete Record"])

with view:
    st.header("Summary")
    df = pd.read_csv('records.csv').sort_values(by="Date", ascending=False)
    copy = df.copy()
    copy["Amount"] = copy["Amount"].abs()

    st.dataframe(
        copy,
        column_config={
            "UUID": st.column_config.Column(width="small"),
            "Amount": st.column_config.NumberColumn("Amount", format="dollar")
        }
    )

with add:
    with st.form("inputRecord", clear_on_submit=True):
        club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")
        name = st.text_input("Item Name:")
        expenseType = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
        amount = st.number_input("Amount ($):", min_value=0.0)
        amount = round(amount, 2)
        date = st.date_input("Date:")
        submit = st.form_submit_button("Submit")

if submit:

    with open('records.csv', 'a', newline="") as file:

        writer = csv.writer(file)
        record_id = str(uuid.uuid4())

        if expenseType == "Income":
            writer.writerow([record_id, club, name, expenseType, amount, date])

        else:
            writer.writerow([record_id, club, name, expenseType, -amount, date,])
    st.success("Submitted!")
    st.rerun()

with delete:
    pass

leave = st.button("Logout")
if leave:
    st.switch_page("app.py")