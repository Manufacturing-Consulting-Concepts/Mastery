#!/usr/bin/env python

import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# Global variables
compliance_framework = "".lower()
custom_framework = False

# df options

# Aggrid options


# Header information
st.title("Mastery")
st.write("Mastery audit preparation through iterative maturity analysis")

# Sidebar menu
st.sidebar.title("Menu")

with st.sidebar:
    framework = st.selectbox("Select a framework",
                             ("CMMC", "ISO 27001", "NIST 800-53", "NIST 800-171", "SOC 2", "SOC 3"))

    if framework == "CMMC":
        compliance_framework = "cmmc"
        st.write("CMMC selected")
    else:
        st.write("**Sorry, framework not yet supported**")

    custom = st.file_uploader("Upload a custom framework", type="csv")
    if custom:
        custom_framework = True

    df = pd.read_csv(f"charts/{compliance_framework}.csv")

    notice = st.write("""
    _Ensure that the CSV is formatted properly_
    
    More information can be found [here]
    """)

    st.subheader("Danger Zone")
    st.button("Reset all Data")

    if custom:
        compliance_framework = custom

# # Main Page

tool, about, docs = st.tabs(["Tool", "About", "Docs"])

# Load the data
# TODO: Add a custom framework option

# Tool Tab
with tool:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Configuration")
        CMMC_Level = st.selectbox("Select Maturity Level", ("1", "2", "3", "All Levels"))
        if CMMC_Level == "1":
            # Select all rows with an L1 Level column
            Level = df.loc[df["Level"] == "L1"]
            Group = st.selectbox("Select a Group", Level["Control Group Name"].unique())
            GroupS = df.loc[df["Control Group Name"] == Group]

            output = GroupS[["Control Group Name", "Practices Name", "Assessment Objectives Order",
                             "Assessment Objectives", "Review"]]

        elif CMMC_Level == "2":
            Level = df.loc[df["Level"] == "L2"]
            Group = st.selectbox("Select a Group", Level["Control Group Name"].unique())
            GroupS = df.loc[df["Control Group Name"] == Group]

            output = GroupS[["Control Group Name", "Practices Name", "Assessment Objectives Order",
                             "Assessment Objectives", "Review"]]

        elif CMMC_Level == "3":
            output = st.write("Sorry, level 3 is not yet available")

        elif CMMC_Level == "All Levels":
            Group = st.selectbox("Select a Group", df["Control Group Name"].unique())

            output = Group[["Control Group Name", "Practices Name", "Assessment Objectives Order",
                            "Assessment Objectives", "Review"]]

    with col2:
        st.write("**Selected Filters**")
        st.write(f"- CMMC Level _{CMMC_Level}_ selected")
        st.write(f"- Control Group _{Group}_ selected")  # Control Group

    table = st.checkbox("Table")
    if table:
        st.dataframe(output, width=1000, height=1000)

    st.write("---")
    mode = st.checkbox("Show quiz mode")

    if mode:
        st.subheader("Quiz Mode")
        True_Review = st.checkbox("Show marked for review")
        if True_Review:
            output = output.loc[df["Review"] == True]
        Objective = st.button("Select Random", key="Objective", help="Select a random objective")

        if Objective:
            random = st.dataframe(output.sample(n=1)["Assessment Objectives"], width=1000, height=2)
            review = st.checkbox("Mark Objective for review")
            notes = st.text_area("Notes", height=100)
            if review:
                output.at[random.index(inplace=True), "Review"] = True
                st.write("Objective marked for review")
