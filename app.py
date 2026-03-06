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

# -----------------------------
# Risk Distribution Chart
# -----------------------------
st.subheader("Risk Level Distribution")

risk_chart = px.pie(
    filtered_df,
    names="Risk_Level",
    title="Container Risk Distribution",
    color="Risk_Level",
    color_discrete_map={
        "Low": "#4CAF50",
        "Critical": "#FF4B4B"
    }
)

risk_chart.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

risk_chart.update_layout(
    title_x=0.35,
    showlegend=True
)

st.plotly_chart(risk_chart, use_container_width=True, key="risk_pie")

# -----------------------------
# Risk Score Histogram
# -----------------------------
st.subheader("Risk Score Distribution")

hist_chart = px.histogram(
    filtered_df,
    x="Risk_Score",
    nbins=25,
    title="Risk Score Distribution",
    color_discrete_sequence=["#1f77b4"]
)

hist_chart.update_layout(
    title_x=0.35,
    xaxis_title="Risk Score",
    yaxis_title="Number of Containers",
    bargap=0.05
)

st.plotly_chart(hist_chart, use_container_width=True, key="risk_hist")

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
