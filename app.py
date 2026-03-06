import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Smart Container Risk Engine",
    page_icon="🚢",
    layout="wide"
)

st.title("🚢 Smart Container Risk Dashboard")

st.markdown("AI-Driven Container Anomaly Detection System")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("container_risk_dataset_1000.csv")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

risk_filter = st.sidebar.multiselect(
    "Select Risk Level",
    options=df["Risk_Level"].unique(),
    default=df["Risk_Level"].unique()
)

country_filter = st.sidebar.multiselect(
    "Origin Country",
    options=df["Origin_Country"].unique(),
    default=df["Origin_Country"].unique()
)

filtered_df = df[
    (df["Risk_Level"].isin(risk_filter)) &
    (df["Origin_Country"].isin(country_filter))
]

# -----------------------------
# KPI Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Containers", len(filtered_df))

col2.metric(
    "Critical Containers",
    (filtered_df["Risk_Level"] == "Critical").sum()
)

col3.metric(
    "Average Risk Score",
    round(filtered_df["Risk_Score"].mean(),2)
)

# -----------------------------
# Risk Distribution Chart
# -----------------------------
st.subheader("Risk Level Distribution")

st.subheader("📊 Container Risk Distribution")

risk_counts = filtered_df["Risk_Level"].value_counts().reset_index()
risk_counts.columns = ["Risk_Level", "Count"]

risk_chart = px.bar(
    risk_counts,
    x="Risk_Level",
    y="Count",
    color="Risk_Level",
    text="Count",
    title="Risk Level Distribution"
)

st.plotly_chart(risk_chart, use_container_width=True)

st.plotly_chart(risk_chart, use_container_width=True)

# -----------------------------
# Risk Score Histogram
# -----------------------------
st.subheader("Risk Score Distribution")

st.subheader("📈 Risk Score Categories")

bins = [0,20,40,60,80,100]
labels = ["0-20","20-40","40-60","60-80","80-100"]

filtered_df["Risk_Range"] = pd.cut(
    filtered_df["Risk_Score"],
    bins=bins,
    labels=labels
)

range_counts = filtered_df["Risk_Range"].value_counts().sort_index().reset_index()
range_counts.columns = ["Risk_Range","Containers"]

range_chart = px.bar(
    range_counts,
    x="Risk_Range",
    y="Containers",
    text="Containers",
    title="Risk Score Distribution"
)

st.plotly_chart(range_chart, use_container_width=True)
st.subheader("🌍 High Risk Containers by Country")

country_chart = px.bar(
    filtered_df,
    x="Origin_Country",
    y="Risk_Score",
    color="Risk_Level",
    title="Risk Score by Country"
)

st.plotly_chart(country_chart, use_container_width=True)
# -----------------------------
# Top Suspicious Containers
# -----------------------------
st.subheader("Top 10 High Risk Containers")

top_containers = filtered_df.sort_values(
    by="Risk_Score",
    ascending=False
).head(10)

st.dataframe(top_containers)

# -----------------------------
# Search Container
# -----------------------------
st.subheader("Search Container")

container_id = st.text_input("Enter Container ID")

if container_id:

    result = df[df["Container_ID"] == container_id]

    if len(result) > 0:
        st.success("Container Found")
        st.dataframe(result)

    else:
        st.error("Container not found")

# -----------------------------
# Full Dataset
# -----------------------------
st.subheader("All Container Records")

st.dataframe(filtered_df)
