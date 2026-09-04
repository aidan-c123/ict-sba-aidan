import streamlit as st
import json
import pandas as pd
import time
import uuid
import numpy as np

login = open("login.json", "r")
data = json.load(login)
login.close()

st.title("Students' Union Financial Dashboard")

df = pd.read_csv('records.csv', index_col=False).sort_values(by="Date", ascending=True)
df["Date"] = pd.to_datetime(df["Date"]).dt.date

if "df" not in st.session_state:
    st.session_state.df = df

st.header("Club Financial Report")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Financial Summary")
    total_income = df[df["Type"]=="Income"]["Amount"].sum()
    total_expense = df[df["Type"]=="Expense"]["Amount"].sum()
    st.write(f"Total income = ${total_income}")
    st.write(f"Total expenditure = ${total_expense}")
    st.write(f"Balance = ${total_income - total_expense}")

with col2:
    st.subheader("Students' Union Financial Summary")
    total_income = df[np.logical_and(df["Type"]=="Income", df["Club"] == "Students' Union")]["Amount"].sum()
    total_expense = df[np.logical_and(df["Type"]=="Expense", df["Club"] == "Students' Union")]["Amount"].sum()
    st.write(f"Total income = ${total_income}")
    st.write(f"Total expenditure = ${total_expense}")
    st.write(f"Balance = ${total_income - total_expense}")

if st.button("Save Changes"):
    missing = st.session_state.df["UUID"].isna() | (st.session_state.df["UUID"] == "")
    st.session_state.df.loc[missing, "UUID"] = [str(uuid.uuid4()) for _ in range(missing.sum())]
    st.session_state.df.to_csv("records.csv", index = False)
    st.success("Saved!")
    time.sleep(1)
    st.rerun()

st.session_state.df = st.data_editor(
    df,
    hide_index=True,
    column_config={
        "Club": st.column_config.SelectboxColumn(options = list(data.keys())),
        "Amount": st.column_config.NumberColumn("Amount", format="dollar"),
        "Date": st.column_config.DateColumn(format="DD.MM.YYYY"),
        "Type": st.column_config.SelectboxColumn(options = ["Income", "Expense"]),
        "UUID": st.column_config.Column(width=1)
    },
    num_rows="dynamic",
    disabled=["UUID"]

)


with st.bottom:
    leave = st.button("Logout")
    if leave:
        st.switch_page("app.py")