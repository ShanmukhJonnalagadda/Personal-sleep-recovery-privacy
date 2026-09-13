"""Public showcase dashboard using synthetic WHOOP-style data only."""

from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_pipeline import filter_by_days, load_demo_data, summary_metrics


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "synthetic_whoop_data.csv"

st.set_page_config(
    page_title="Sleep & Recovery Analytics",
    page_icon="📈",
    layout="wide",
)

st.title("Personal Sleep & Recovery Analytics Dashboard")
st.caption("Public showcase • Synthetic demonstration data • Not medical advice")

period = st.selectbox(
    "Analysis period",
    options=["30 days", "90 days", "All data"],
    index=1,
)
days = {"30 days": 30, "90 days": 90, "All data": None}[period]

data = filter_by_days(load_demo_data(DATA_PATH), days)
metrics = summary_metrics(data)

columns = st.columns(5)
formats = {
    "Recovery": "{:.0f}%",
    "HRV": "{:.0f} ms",
    "Resting HR": "{:.0f} bpm",
    "Sleep performance": "{:.0f}%",
    "Day strain": "{:.1f}",
}
for column, (name, value) in zip(columns, metrics.items()):
    column.metric(name, formats[name].format(value))

st.subheader("Recovery trends and physiological insights")
trend = go.Figure()
trend.add_trace(
    go.Scatter(
        x=data["cycle_date"],
        y=data["recovery_score"],
        name="Daily recovery",
        mode="lines+markers",
        line={"color": "#00b87c", "width": 2},
        marker={"size": 5},
    )
)
trend.add_trace(
    go.Scatter(
        x=data["cycle_date"],
        y=data["recovery_7d"],
        name="7-day average",
        line={"color": "#276ef1", "width": 3},
    )
)
trend.update_layout(
    xaxis_title="Cycle date",
    yaxis_title="Recovery score (%)",
    hovermode="x unified",
    margin={"l": 20, "r": 20, "t": 20, "b": 20},
)
st.plotly_chart(trend, width="stretch")

left, right = st.columns(2)
with left:
    st.subheader("Sleep quality and recovery")
    sleep_chart = px.scatter(
        data,
        x="sleep_duration_hr",
        y="recovery_score",
        color="sleep_performance_pct",
        color_continuous_scale="Viridis",
        labels={
            "sleep_duration_hr": "Sleep duration (hours)",
            "recovery_score": "Recovery score (%)",
            "sleep_performance_pct": "Sleep performance (%)",
        },
    )
    st.plotly_chart(sleep_chart, width="stretch")

with right:
    st.subheader("Strain–recovery relationship")
    strain_chart = px.scatter(
        data.dropna(subset=["next_cycle_recovery"]),
        x="day_strain",
        y="next_cycle_recovery",
        labels={
            "day_strain": "Day strain",
            "next_cycle_recovery": "Next-cycle recovery (%)",
        },
        color_discrete_sequence=["#ff8a00"],
    )
    st.plotly_chart(strain_chart, width="stretch")
    st.caption("Synthetic associations are illustrative, not causal or predictive evidence.")

with st.expander("View synthetic records"):
    st.dataframe(data, width="stretch", hide_index=True)
