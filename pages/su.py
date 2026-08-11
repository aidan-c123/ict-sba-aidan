import streamlit as st
import json
import csv
import uuid
import pandas as pd
import time

login = open("login.json", "r")
data = json.load(login)
login.close()

st.title("Students' Union Financial Dashboard")

view, add, delete = st.tabs(["View Records", "Add Record", "Delete Record"])

df = pd.read_csv('records.csv', index_col=False).sort_values(by="Date", ascending=True)
copy = df.copy()
copy["Amount"] = copy["Amount"].abs()

with view:
    st.header("Summary")
    
    st.dataframe(
        copy,
        hide_index=True,
        column_config={
            "UUID": st.column_config.Column(width=25),
            "Amount": st.column_config.NumberColumn("Amount", format="dollar")
        }
    )

with add:
    with st.form("inputRecord", clear_on_submit=True):
        club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")
        name = st.text_input("Item Name:")
        expense_type = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
        amount = st.number_input("Amount ($):", min_value=0.0)
        amount = round(amount, 2)
        date = st.date_input("Date:")
        add_submit = st.form_submit_button("Submit")

if add_submit:

    with open('records.csv', 'a', newline="") as file:

        writer = csv.writer(file)
        record_id = str(uuid.uuid4())

        if expense_type == "Income":
            writer.writerow([record_id, club, name, expense_type, amount, date])

        else:
            writer.writerow([record_id, club, name, expense_type, -amount, date,])
    st.success("Submitted!")
    time.sleep(2)
    st.rerun()

with delete:
    if 'del_confirm' not in st.session_state:
        st.session_state.del_confirm = False
    if 'del_uuid' not in st.session_state:
        st.session_state.del_uuid = ""

    with st.form("deleteRecord", clear_on_submit=True):
        uuid = st.text_input("UUID of the record to delete:")
        del_submit = st.form_submit_button("Submit")

        if del_submit and uuid:
            st.session_state.del_uuid = uuid
            st.session_state.del_confirm = True

    if st.session_state.del_confirm and st.session_state.del_uuid:
        st.write("This is the record that will be deleted:")

        if copy[copy["UUID"] == st.session_state.del_uuid].empty:
            st.warning("No record found with that UUID")
            del_clear = st.button("Clear")
            if del_clear:
                st.session_state.del_confirm = False
                st.session_state.del_uuid = ""
                st.rerun()
        else:
            st.dataframe(
            copy[copy["UUID"] == uuid],
            hide_index=True,
            column_config={
                "UUID": st.column_config.Column(width=25),
                "Amount": st.column_config.NumberColumn("Amount", format="dollar")
                }
            )
            del_confirm = st.button("Confirm")
            if del_confirm:
                df = df[df["UUID"] != uuid]
                df.to_csv("records.csv", index=False)
                st.success("Record deleted successfully!")
                time.sleep(2)
                st.session_state.del_confirm = False
                st.session_state.del_uuid = ""
                st.rerun()
        



with st.bottom:
    leave = st.button("Logout")
    if leave:
        st.switch_page("app.py")