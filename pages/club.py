import streamlit as st
import json
import pandas as pd
import uuid
import time
import numpy as np

f = open("id.txt", "r")
info = f.readlines()
f.close()
club = info[0].strip()

st.title(f"{club} Financial Dashboard")

df = pd.read_csv('records.csv', index_col=False).sort_values(by="Date", ascending=True)
df["Date"] = pd.to_datetime(df["Date"]).dt.date

if "df" not in st.session_state:
    st.session_state.df = df

st.header("Club Financial Report")

st.subheader(f"{club} Financial Summary")
total_income = df[np.logical_and(df["Type"]=="Income", df["Club"] == "Students' Union")]["Amount"].sum()
total_expense = df[np.logical_and(df["Type"]=="Expense", df["Club"] == "Students' Union")]["Amount"].sum()
st.write(f"Total income = ${total_income}")
st.write(f"Total expenditure = ${total_expense}")
st.write(f"Balance = ${total_income - total_expense}")

if st.button("Save Changes"):
    st.session_state.df.to_csv("records.csv", index = False)
    st.success("Saved!")
    time.sleep(1)
    st.rerun()

st.session_state.df = st.data_editor(
    df[df["Club"]==club],
    hide_index=True,
    column_config={
        "Club": st.column_config.SelectboxColumn(options = [club]),
        "Amount": st.column_config.NumberColumn("Amount", format="dollar"),
        "Date": st.column_config.DateColumn(format="DD.MM.YYYY"),
        "Type": st.column_config.SelectboxColumn(options = ["Income", "Expense"])
    },
    num_rows="dynamic"
)

with st.bottom:
    leave = st.button("Logout")
    if leave:
        st.switch_page("app.py")