import streamlit as st
import json
import csv
import uuid
import pandas as pd
import time
import plotly.express as px

login = open("login.json", "r")
data = json.load(login)
login.close()

st.title("Students' Union Financial Dashboard")

total_summary, club_summary, view, edit_records, edit_users = st.tabs(["View Master Summary", "View Club Summary", "View Records", "Edit Records", "Edit Users"])

df = pd.read_csv('records.csv', index_col=False).sort_values(by="Date", ascending=True)
copy = df.copy()
su_copy = df.copy()[df["Club"] == "Students' Union"]

cat = pd.read_csv('categories.csv', index_col=False)

with total_summary:

    copy["Income_Amt"] = copy["Amount"].where(copy["Type"] == "Income", 0)
    copy["Expense_Amt"] = copy["Amount"].where(copy["Type"] == "Expense", 0)

    copy["Cumulative Income"] = copy["Income_Amt"].cumsum()
    copy["Cumulative Expense"] = copy["Expense_Amt"].cumsum()
    copy["Cumulative Balance"] = copy["Cumulative Income"] - copy["Cumulative Expense"]

    st.subheader("Total Financial Summary")
    total_income = copy[copy["Type"]=="Income"]["Amount"].sum()
    total_expense = copy[copy["Type"]=="Expense"]["Amount"].sum()
    st.write(f"Total income = {total_income}")
    st.write(f"Total expenditure = {total_expense}")
    st.write(f"Balance = {total_income - total_expense}")

    st.subheader("Total Balance over Time")
    st.line_chart(copy, x="Date", y=["Cumulative Income", "Cumulative Expense", "Cumulative Balance"])

    col1, col2 = st.columns(2)

    with col1:
        income_pie = px.pie(copy[copy["Type"]=="Income"], values="Income_Amt", names="Category", title="Total Income by Category")
        st.plotly_chart(income_pie)
    with col2:
        expense_pie = px.pie(copy[copy["Type"]=="Expense"], values="Expense_Amt", names="Category", title="Total Expense by Category")
        st.plotly_chart(expense_pie)
        expense_pie.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)



with club_summary:

    su_copy["Income_Amt"] = su_copy["Amount"].where(su_copy["Type"] == "Income", 0)
    su_copy["Expense_Amt"] = su_copy["Amount"].where(su_copy["Type"] == "Expense", 0)

    su_copy["Cumulative Income"] = su_copy["Income_Amt"].cumsum()
    su_copy["Cumulative Expense"] = su_copy["Expense_Amt"].cumsum()
    su_copy["Cumulative Balance"] = su_copy["Cumulative Income"] - su_copy["Cumulative Expense"]

    st.subheader("Student's Union Financial Summary")
    total_income = su_copy[su_copy["Type"]=="Income"]["Amount"].sum()
    total_expense = su_copy[su_copy["Type"]=="Expense"]["Amount"].sum()
    st.write(f"Total income = {total_income}")
    st.write(f"Total expenditure = {total_expense}")
    st.write(f"Balance = {total_income - total_expense}")


    st.subheader("Total Balance over Time")
    st.line_chart(su_copy, x="Date", y=["Cumulative Income", "Cumulative Expense", "Cumulative Balance"])

    col1, col2 = st.columns(2)

    with col1:
        clubincome_pie = px.pie(su_copy[su_copy["Type"]=="Income"], values="Income_Amt", names="Category", title="Total Income by Category")
        st.plotly_chart(clubincome_pie, key="erkghhgoirhgeoirrex")
    with col2:
        clubexpense_pie = px.pie(su_copy[su_copy["Type"]=="Expense"], values="Expense_Amt", names="Category", title="Total Expense by Category")
        st.plotly_chart(clubexpense_pie, key='zdfkghzd fdku')

with view:
    st.header("Clubs' Financial Report")

    st.dataframe(
        df,
        hide_index=True,
        column_config={
            "UUID": st.column_config.Column(width=25),
            "Amount": st.column_config.NumberColumn("Amount", format="dollar")
        }
    )

with edit_records:
    add, update, delete = st.tabs(["Add Record", "Update Record", "Delete Record"])
    with add:
        with st.form("inputRecord", clear_on_submit=True):
            club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")
            name = st.text_input("Item Name:")
            category = st.selectbox("Item Category", list(cat["Name"]), placeholder="Select category...", index=None)
            expense_type = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
            amount = st.number_input("Amount ($):", min_value=0.0)
            date = str(st.date_input("Date:"))
            add_submit = st.form_submit_button("Submit")

    if add_submit:
        with open('records.csv', 'a', newline="") as file:

            writer = csv.writer(file)
            record_id = str(uuid.uuid4())
            writer.writerow([club, name, category, expense_type, amount, date, record_id])

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
                    club = st.selectbox("Club:", list(data.keys()), index=None, placeholder="Select club...")
                    name = st.text_input("Item Name:")
                    category = st.selectbox("Item Category", list(cat["Name"]), placeholder="Select category...", index = None)
                    expense_type = st.radio("Is this an income or expense?", ["Income", "Expense"], index=None, horizontal=True)
                    amount = st.number_input("Amount ($):", min_value=0.0, value=None)
                    date = str(st.date_input("Date:", value = None))
                    update_confirm = st.form_submit_button("Confirm")

                if update_confirm:
                    update_dict = {"Club" : club, "Item Name": name, "Category": category, "Type" : expense_type, "Amount": amount,"Date": date}
                    
                    for i in list(update_dict.keys()):
                        if update_dict[i] is not None and update_dict[i] != "":
                            df.loc[df["UUID"] == st.session_state.update_uuid, i] = update_dict[i]
                            df.loc[df["UUID"] == st.session_state.update_uuid, "Amount"] = abs(df.loc[df["UUID"] == st.session_state.update_uuid, "Amount"])

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

            if df[df["UUID"] == st.session_state.del_uuid].empty:
                st.warning("No record found with that UUID")
                del_clear = st.button("Clear")
                if del_clear:
                    st.session_state.del_confirm = False
                    st.session_state.del_uuid = ""
                    st.rerun()
            else:
                st.dataframe(
                df[df["UUID"] == st.session_state.del_uuid],
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


with edit_users:
    login = open("login.json", "r")
    users = pd.DataFrame.from_dict(dict(json.load(login)), orient="index", columns=["Password"])
    users = users.reset_index().rename(columns={"index": "Club"})
    login.close()

    if st.button("Save Changes"):
        users.update(st.session_state.users)
        updated_dict = st.session_state.users.set_index("Club")["Password"].to_dict()

        with open("login.json", "w") as login:
            json.dump(updated_dict, login, indent=4)

        st.success("Saved!")
        time.sleep(1)
        st.rerun()
    
    st.session_state.users = st.data_editor(users, hide_index=True, num_rows="dynamic")

    


with st.bottom:
    leave = st.button("Logout")
    if leave:
        st.switch_page("app.py")