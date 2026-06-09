import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = "data/processed/rtt_incomplete_provider_clean.csv"

st.set_page_config(
    page_title="NHS RTT Waiting List Dashboard",
    layout="wide"
)

st.title("NHS RTT Waiting List Intelligence Dashboard")
st.caption("Provider-level incomplete pathway analysis | March 2026")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["reporting_month"])
    return df

df = load_data()

# Remove national total rows from specialty analysis
specialty_df = df[df["treatment_function"] != "Total"].copy()

# Sidebar filters
st.sidebar.header("Filters")

providers = sorted(df["provider_name"].dropna().unique())
selected_provider = st.sidebar.selectbox(
    "Select Provider",
    ["All Providers"] + providers
)

if selected_provider != "All Providers":
    filtered_df = df[df["provider_name"] == selected_provider]
    specialty_filtered = specialty_df[specialty_df["provider_name"] == selected_provider]
else:
    filtered_df = df
    specialty_filtered = specialty_df

# KPI calculations
total_waiting = filtered_df["total_incomplete_pathways"].sum()
within_18 = filtered_df["total_within_18_weeks"].sum()
pct_within_18 = within_18 / total_waiting if total_waiting else 0
waits_52 = filtered_df["total_52_plus"].sum()
waits_65 = filtered_df["total_65_plus"].sum()
waits_78 = filtered_df["total_78_plus"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Waiting List", f"{total_waiting:,.0f}")
col2.metric("% Within 18 Weeks", f"{pct_within_18:.2%}")
col3.metric("52+ Week Waits", f"{waits_52:,.0f}")
col4.metric("78+ Week Waits", f"{waits_78:,.0f}")

st.divider()

# Top providers
if selected_provider == "All Providers":
    st.subheader("Top 10 Providers by Waiting List Size")

    top_providers = (
        df.groupby("provider_name", as_index=False)["total_incomplete_pathways"]
        .sum()
        .sort_values("total_incomplete_pathways", ascending=False)
        .head(10)
    )

    fig_provider = px.bar(
        top_providers,
        x="total_incomplete_pathways",
        y="provider_name",
        orientation="h",
        title="Top 10 Providers by Total Waiting List",
        labels={
            "total_incomplete_pathways": "Total Waiting List",
            "provider_name": "Provider"
        }
    )
    fig_provider.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_provider, use_container_width=True)

# Specialty analysis
st.subheader("Top Treatment Functions by Waiting List Size")

top_specialties = (
    specialty_filtered.groupby("treatment_function", as_index=False)
    .agg(
        total_waiting_list=("total_incomplete_pathways", "sum"),
        total_52_plus=("total_52_plus", "sum")
    )
    .sort_values("total_waiting_list", ascending=False)
    .head(10)
)

fig_specialty = px.bar(
    top_specialties,
    x="total_waiting_list",
    y="treatment_function",
    orientation="h",
    title="Top Treatment Functions by Waiting List Size",
    labels={
        "total_waiting_list": "Total Waiting List",
        "treatment_function": "Treatment Function"
    }
)
fig_specialty.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_specialty, use_container_width=True)

# Long waits
st.subheader("52+ Week Wait Pressure")

long_waits = (
    specialty_filtered.groupby(["provider_name", "treatment_function"], as_index=False)
    .agg(
        total_waiting_list=("total_incomplete_pathways", "sum"),
        waits_52_plus=("total_52_plus", "sum")
    )
)

long_waits["pct_52_plus"] = (
    long_waits["waits_52_plus"] / long_waits["total_waiting_list"]
)

long_waits = long_waits[
    long_waits["total_waiting_list"] > 0
].sort_values("pct_52_plus", ascending=False).head(20)

fig_long = px.bar(
    long_waits,
    x="pct_52_plus",
    y="provider_name",
    color="treatment_function",
    orientation="h",
    title="Top Provider-Specialty Combinations by 52+ Week Wait Proportion",
    labels={
        "pct_52_plus": "% 52+ Week Waits",
        "provider_name": "Provider"
    }
)
fig_long.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_long, use_container_width=True)

# Data table
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)
