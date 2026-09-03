import streamlit as st
import json
import csv
import uuid
import pandas as pd
import time
import numpy as np

f = open("id.txt", "r")
info = f.readlines()
f.close()
club = info[0].strip()

st.title(f"{club} Financial Dashboard")

view, add, update, delete = st.tabs(["View Records", "Add Record", "Update record", "Delete Record"])

df = pd.read_csv('records.csv', index_col=False).sort_values(by="Date", ascending=True)
copy = df.copy()[df["Club"] == club]
copy["Amount"] = copy["Amount"].abs()

with view:
    st.header(f"{club} Financial Report")

    st.subheader("Students' Union Financial Summary")
    total_income = df[np.logical_and(df["Type"]=="Income", df["Club"] == club)]["Amount"].sum()
    total_expense = -df[np.logical_and(df["Type"]=="Expense", df["Club"] == club)]["Amount"].sum()
    st.write(f"Total income = {total_income}")
    st.write(f"Total expenditure = {total_expense}")
    st.write(f"Balance = {total_income - total_expense}")
    
    
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
        name = st.text_input("Item Name:")
        expense_type = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
        amount = st.number_input("Amount ($):", min_value=0.0)
        date = st.date_input("Date:")
        add_submit = st.form_submit_button("Submit")

if add_submit:
    with open('records.csv', 'a', newline="") as file:

        writer = csv.writer(file)
        record_id = str(uuid.uuid4())

        if expense_type == "Income":
            writer.writerow([record_id, club, name, expense_type, amount, date])

        else:
            writer.writerow([record_id, club, name, expense_type, -amount, date])
    st.success("Submitted!")
    time.sleep(2)
    st.rerun()



with update:
    if 'update_confirm' not in st.session_state:
        st.session_state.update_confirm = False
    if 'update_uuid' not in st.session_state:
        st.session_state.update_uuid = ""

    with st.form("update", clear_on_submit=True):
        uuid = st.text_input("UUID of the record to update:")
        update_submit = st.form_submit_button("Submit")

        if update_submit and uuid:
            st.session_state.update_uuid = uuid
            st.session_state.update_confirm = True

    if st.session_state.update_confirm and st.session_state.update_uuid:
        st.write("This is the record that will be updated:")

        if copy[copy["UUID"] == st.session_state.update_uuid].empty:
            st.warning("No record found with that UUID")
            update_clear = st.button("Clear")
            if update_clear:
                st.session_state.update_confirm = False
                st.session_state.update_uuid = ""
                st.rerun()
        else:
            st.dataframe(
            copy[copy["UUID"] == st.session_state.update_uuid],
            hide_index=True,
            column_config={
                "UUID": st.column_config.Column(width=25),
                "Amount": st.column_config.NumberColumn("Amount", format="dollar")
                }
            )

            with st.form("update_items", clear_on_submit=True):
                st.write("Leave input blank if it is not needed to be updated:")
                name = st.text_input("Item Name:")
                expense_type = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
                amount = st.number_input("Amount ($):", min_value=0.0, value=None)
                date = st.date_input("Date:", value = None)
                update_confirm = st.form_submit_button("Confirm")

            if update_confirm:
                if expense_type == "Income" or amount == None:
                    update_dict = {"Club" : club, "Item Name": name, "Type" : expense_type, "Amount": amount,"Date": date}

                else:
                    update_dict = {"Club" : club, "Item Name": name, "Type" : expense_type, "Amount": -amount,"Date": date}
                
                for i in list(update_dict.keys()):
                    if update_dict[i] is not None and update_dict[i] != "":
                        df.loc[df["UUID"] == st.session_state.update_uuid, i] = update_dict[i]
                        if i == "Type" and update_dict[i] == "Income" and update_dict["Amount"] == None:
                            df.loc[df["UUID"] == st.session_state.update_uuid, "Amount"] = abs(df.loc[df["UUID"] == st.session_state.update_uuid, "Amount"])
                        elif i == "Type" and update_dict[i] == "Expense" and update_dict["Amount"] == None:
                            df.loc[df["UUID"] == st.session_state.update_uuid, "Amount"] = -abs(df.loc[df["UUID"] == st.session_state.update_uuid, "Amount"])
                
                df.to_csv("records.csv", index=False)
                st.success("Record updated successfully!")
                time.sleep(2)
                st.session_state.update_confirm = False
                st.session_state.update_uuid = ""
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
            copy[copy["UUID"] == st.session_state.del_uuid],
            hide_index=True,
            column_config={
                "UUID": st.column_config.Column(width=25),
                "Amount": st.column_config.NumberColumn("Amount", format="dollar")
                }
            )
            del_confirm = st.button("Confirm")
            if del_confirm:
                df = df[df["UUID"] != st.session_state.del_uuid]
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