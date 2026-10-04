import streamlit as st
import pandas as pd
import plotly.express as px
import os


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Smart Street Lighting",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================================
# HIGH-TECH DARK THEME
# ==========================================================

st.markdown("""
<style>

/* ========================================================
   MAIN BACKGROUND
   ======================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(0, 229, 255, 0.08),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(124, 58, 237, 0.10),
            transparent 25%
        ),
        #07111f;
}


/* Main content spacing */

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}


/* ========================================================
   SIDEBAR
   ======================================================== */

section[data-testid="stSidebar"] {
    background: #050b14 !important;
    border-right: 1px solid #1e3a5f !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #e5f7ff !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label {
    color: #a8c0d6 !important;
}


/* ========================================================
   TITLE
   ======================================================== */

h1 {
    color: #e8faff !important;
    font-size: 36px !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px;
}

h2 {
    color: #d9f7ff !important;
}

h3 {
    color: #c8e9f5 !important;
}


/* ========================================================
   SUBTITLE
   ======================================================== */

.subtitle-text {
    color: #8faec4;
    font-size: 15px;
    margin-top: -12px;
    margin-bottom: 20px;
}


/* ========================================================
   NATIVE STREAMLIT METRIC CARDS
   ======================================================== */

[data-testid="stMetric"] {
    background:
        linear-gradient(
            145deg,
            #0d1b2e,
            #0a1626
        ) !important;

    border: 1px solid #1d4163 !important;

    border-radius: 15px !important;

    padding: 18px 18px !important;

    box-shadow:
        0 0 15px rgba(0, 229, 255, 0.06),
        inset 0 0 20px rgba(0, 229, 255, 0.02);
}


/* Metric labels */

[data-testid="stMetricLabel"] {
    color: #82a9c2 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}


/* Metric values */

[data-testid="stMetricValue"] {
    color: #f1fbff !important;
    font-size: 27px !important;
    font-weight: 800 !important;
}


/* ========================================================
   SUCCESS MESSAGE
   ======================================================== */

[data-testid="stAlert"] {
    background: rgba(16, 185, 129, 0.10) !important;
    border: 1px solid rgba(16, 185, 129, 0.35) !important;
    color: #7fffd4 !important;
}


/* ========================================================
   MULTISELECT
   ======================================================== */

[data-baseweb="select"] > div {
    background-color: #0d1828 !important;
    border-color: #21405e !important;
}


/* ========================================================
   BUTTON
   ======================================================== */

.stDownloadButton button {
    background: linear-gradient(
        90deg,
        #0891b2,
        #7c3aed
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 9px !important;

    font-weight: 700 !important;
}


/* ========================================================
   DATAFRAME
   ======================================================== */

[data-testid="stDataFrame"] {
    border: 1px solid #1d4163;
    border-radius: 10px;
}


/* ========================================================
   DIVIDER
   ======================================================== */

hr {
    border-color: #1c354d !important;
}


/* ========================================================
   FOOTER
   ======================================================== */

.footer-text {
    text-align: center;
    color: #607d94;
    font-size: 12px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# DATA PATH
# ==========================================================

 DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data"
)

street_file = os.path.join(
    DATASET_PATH,
    "street_light_data.csv"
)


# ==========================================================
# CHECK FILE
# ==========================================================

if not os.path.exists(street_file):

    st.error(
        "street_light_data.csv was not found."
    )

    st.code(street_file)

    st.stop()


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data(path):

    return pd.read_csv(path)


df = load_data(street_file)


# ==========================================================
# CLEAN COLUMN NAMES
# ==========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)


# ==========================================================
# CLEAN CATEGORICAL DATA
# ==========================================================

categorical_columns = [
    "location",
    "traffic_level",
    "light_status",
    "fault_status"
]

for column in categorical_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.replace(
                "\xa0",
                " ",
                regex=False
            )
            .str.strip()
        )

        df[column] = df[column].replace(
            [
                "",
                "nan",
                "NaN",
                "None",
                "NULL",
                "null"
            ],
            pd.NA
        )


# ==========================================================
# TRAFFIC STANDARDIZATION
# ==========================================================

if "traffic_level" in df.columns:

    df["traffic_level"] = (
        df["traffic_level"]
        .str.strip()
        .str.title()
    )

    df["traffic_level"] = df[
        "traffic_level"
    ].where(
        df["traffic_level"].isin(
            [
                "Low",
                "Medium",
                "High"
            ]
        )
    )


# ==========================================================
# LIGHT STATUS
# ==========================================================

if "light_status" in df.columns:

    df["light_status"] = (
        df["light_status"]
        .str.strip()
        .str.upper()
    )


# ==========================================================
# FAULT STATUS
# ==========================================================

if "fault_status" in df.columns:

    df["fault_status"] = (
        df["fault_status"]
        .str.strip()
        .str.upper()
    )


# ==========================================================
# NUMERIC COLUMNS
# ==========================================================

numeric_columns = [
    "power_consumption",
    "brightness_level",
    "motion_detected",
    "voltage",
    "current",
    "temperature",
    "ldr_value",
    "latitude",
    "longitude"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ==========================================================
# TIMESTAMP
# ==========================================================

if "timestamp" in df.columns:

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )


# ==========================================================
# HEADER
# ==========================================================

st.title("💡 Smart Street Lighting")

st.markdown(
    '<p class="subtitle-text">'
    'Real-time energy monitoring and intelligent '
    'street-light analytics'
    '</p>',
    unsafe_allow_html=True
)

st.success(
    f"✓ {len(df):,} street-light records loaded successfully"
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙️ Dashboard Filters")

st.sidebar.caption(
    "Explore and analyze street-light data"
)


# Location

location_values = sorted(
    df["location"]
    .dropna()
    .unique()
    .tolist()
)

selected_locations = st.sidebar.multiselect(
    "📍 Location",
    location_values,
    default=location_values
)


# Traffic

traffic_values = [
    "Low",
    "Medium",
    "High"
]

selected_traffic = st.sidebar.multiselect(
    "🚦 Traffic Level",
    traffic_values,
    default=traffic_values
)


# Light Status

status_values = sorted(
    df["light_status"]
    .dropna()
    .unique()
    .tolist()
)

selected_status = st.sidebar.multiselect(
    "💡 Light Status",
    status_values,
    default=status_values
)


# Fault Status

fault_values = sorted(
    df["fault_status"]
    .dropna()
    .unique()
    .tolist()
)

selected_fault = st.sidebar.multiselect(
    "⚠️ Fault Status",
    fault_values,
    default=fault_values
)


# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = df.copy()


if selected_locations:

    filtered = filtered[
        filtered["location"].isin(
            selected_locations
        )
    ]


if selected_traffic:

    filtered = filtered[
        filtered["traffic_level"].isin(
            selected_traffic
        )
    ]


if selected_status:

    filtered = filtered[
        filtered["light_status"].isin(
            selected_status
        )
    ]


if selected_fault:

    filtered = filtered[
        filtered["fault_status"].isin(
            selected_fault
        )
    ]


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_lights = (
    filtered["light_id"]
    .nunique()
)

total_power = (
    filtered["power_consumption"]
    .sum()
)

average_power = (
    filtered["power_consumption"]
    .mean()
)

active_lights = (
    filtered[
        filtered["light_status"] == "ON"
    ]["light_id"]
    .nunique()
)

faulty_lights = (
    filtered[
        filtered["fault_status"]
        .astype("string")
        .str.upper()
        .ne("NORMAL")
    ]["light_id"]
    .nunique()
)


# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📊 System Overview")

c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(
        "💡 Total Lights",
        f"{total_lights:,}"
    )


with c2:

    st.metric(
        "⚡ Total Energy",
        f"{total_power:,.0f}"
    )


with c3:

    st.metric(
        "📈 Average Power",
        f"{average_power:.2f}"
    )


with c4:

    st.metric(
        "🟢 Active Lights",
        f"{active_lights:,}"
    )


with c5:

    st.metric(
        "⚠️ Faulty Lights",
        f"{faulty_lights:,}"
    )


# ==========================================================
# TRAFFIC OVERVIEW
# ==========================================================

st.divider()

st.subheader("🚦 Traffic Overview")

traffic_counts = (
    filtered["traffic_level"]
    .dropna()
    .value_counts()
)


t1, t2, t3 = st.columns(3)


with t1:

    st.metric(
        "Low Traffic",
        f"{traffic_counts.get('Low', 0):,}"
    )


with t2:

    st.metric(
        "Medium Traffic",
        f"{traffic_counts.get('Medium', 0):,}"
    )


with t3:

    st.metric(
        "High Traffic",
        f"{traffic_counts.get('High', 0):,}"
    )


# ==========================================================
# CHART COLOR PALETTE
# ==========================================================

NEON = [
    "#00E5FF",
    "#7C3AED",
    "#22C55E",
    "#F59E0B",
    "#F43F5E",
    "#38BDF8"
]


# ==========================================================
# ENERGY MONITORING
# ==========================================================

st.divider()

st.subheader("⚡ Energy Monitoring")

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# POWER TREND
# ----------------------------------------------------------

with col1:

    power_time = (
        filtered
        .dropna(
            subset=[
                "timestamp",
                "power_consumption"
            ]
        )
        .groupby(
            "timestamp",
            as_index=False
        )["power_consumption"]
        .sum()
        .sort_values("timestamp")
    )

    fig = px.line(
        power_time,
        x="timestamp",
        y="power_consumption",
        title="Power Consumption Over Time"
    )

    fig.update_traces(
        line=dict(
            color="#00E5FF",
            width=3
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        ),
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ----------------------------------------------------------
# LOCATION ENERGY
# ----------------------------------------------------------

with col2:

    location_power = (
        filtered
        .dropna(
            subset=[
                "location",
                "power_consumption"
            ]
        )
        .groupby(
            "location",
            as_index=False
        )["power_consumption"]
        .sum()
        .sort_values(
            "power_consumption",
            ascending=False
        )
    )

    fig = px.bar(
        location_power,
        x="location",
        y="power_consumption",
        title="Energy Consumption by Location",
        text_auto=".2s",
        color="location",
        color_discrete_sequence=NEON
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        ),
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# TRAFFIC ANALYSIS
# ==========================================================

st.divider()

st.subheader("🚦 Traffic & Lighting Analysis")

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# TRAFFIC DISTRIBUTION
# ----------------------------------------------------------

with col1:

    traffic_chart = (
        filtered[
            filtered["traffic_level"].isin(
                [
                    "Low",
                    "Medium",
                    "High"
                ]
            )
        ]
        .groupby(
            "traffic_level",
            observed=True
        )
        .size()
        .reindex(
            [
                "Low",
                "Medium",
                "High"
            ],
            fill_value=0
        )
        .reset_index(
            name="Records"
        )
    )

    fig = px.bar(
        traffic_chart,
        x="traffic_level",
        y="Records",
        title="Traffic Level Distribution",
        text="Records",
        color="traffic_level",
        color_discrete_map={
            "Low": "#22C55E",
            "Medium": "#F59E0B",
            "High": "#F43F5E"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        ),
        showlegend=False,
        xaxis=dict(
            categoryorder="array",
            categoryarray=[
                "Low",
                "Medium",
                "High"
            ]
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ----------------------------------------------------------
# TRAFFIC VS POWER
# ----------------------------------------------------------

with col2:

    traffic_power = (
        filtered[
            filtered["traffic_level"].isin(
                [
                    "Low",
                    "Medium",
                    "High"
                ]
            )
        ]
        .dropna(
            subset=[
                "power_consumption"
            ]
        )
        .groupby(
            "traffic_level",
            observed=True
        )["power_consumption"]
        .mean()
        .reindex(
            [
                "Low",
                "Medium",
                "High"
            ]
        )
        .reset_index()
    )

    traffic_power.columns = [
        "Traffic Level",
        "Average Power"
    ]

    fig = px.bar(
        traffic_power,
        x="Traffic Level",
        y="Average Power",
        title="Average Power by Traffic Level",
        text_auto=".2f",
        color="Traffic Level",
        color_discrete_map={
            "Low": "#22C55E",
            "Medium": "#F59E0B",
            "High": "#F43F5E"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# SMART LIGHTING BEHAVIOUR
# ==========================================================

st.divider()

st.subheader("💡 Smart Lighting Behaviour")

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# MOTION
# ----------------------------------------------------------

with col1:

    motion_power = (
        filtered
        .dropna(
            subset=[
                "motion_detected",
                "power_consumption"
            ]
        )
        .groupby(
            "motion_detected",
            as_index=False
        )["power_consumption"]
        .mean()
    )

    motion_power["Motion"] = (
        motion_power[
            "motion_detected"
        ]
        .map({
            0: "No Motion",
            1: "Motion Detected"
        })
    )

    fig = px.bar(
        motion_power,
        x="Motion",
        y="power_consumption",
        title="Average Power vs Motion",
        text_auto=".2f",
        color="Motion",
        color_discrete_sequence=[
            "#7C3AED",
            "#00E5FF"
        ]
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        height=380,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ----------------------------------------------------------
# BRIGHTNESS
# ----------------------------------------------------------

with col2:

    brightness_data = (
        filtered
        .dropna(
            subset=[
                "brightness_level"
            ]
        )
    )

    fig = px.histogram(
        brightness_data,
        x="brightness_level",
        nbins=20,
        title="Brightness Level Distribution"
    )

    fig.update_traces(
        marker_color="#A855F7"
    )

    fig.update_layout(
        template="plotly_dark",
        height=380,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# SYSTEM HEALTH
# ==========================================================

st.divider()

st.subheader("🛠️ System Health")

col1, col2 = st.columns(2)


# ----------------------------------------------------------
# LIGHT STATUS
# ----------------------------------------------------------

with col1:

    status_data = (
        filtered["light_status"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    status_data.columns = [
        "Status",
        "Count"
    ]

    fig = px.pie(
        status_data,
        names="Status",
        values="Count",
        hole=0.58,
        title="Light Status",
        color="Status",
        color_discrete_map={
            "ON": "#22C55E",
            "OFF": "#64748B"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ----------------------------------------------------------
# FAULT STATUS
# ----------------------------------------------------------

with col2:

    fault_data = (
        filtered["fault_status"]
        .dropna()
        .value_counts()
        .reset_index()
    )

    fault_data.columns = [
        "Fault Status",
        "Count"
    ]

    fig = px.bar(
        fault_data,
        x="Fault Status",
        y="Count",
        title="Fault Status Distribution",
        text="Count",
        color="Fault Status",
        color_discrete_map={
            "NORMAL": "#22C55E",
            "FAULT": "#F43F5E"
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        height=390,
        paper_bgcolor="#0b1727",
        plot_bgcolor="#0b1727",
        font=dict(
            color="#d9f7ff"
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================================
# RECENT DATA
# ==========================================================

st.divider()

st.subheader("📋 Recent Street Light Records")

display_columns = [
    "timestamp",
    "light_id",
    "location",
    "traffic_level",
    "motion_detected",
    "brightness_level",
    "power_consumption",
    "temperature",
    "light_status",
    "fault_status"
]

display_columns = [
    col
    for col in display_columns
    if col in filtered.columns
]

recent_data = (
    filtered[
        display_columns
    ]
    .sort_values(
        "timestamp",
        ascending=False
    )
    .head(100)
)

st.dataframe(
    recent_data,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# DOWNLOAD
# ==========================================================

st.subheader("📥 Export Data")

csv_data = filtered.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="street_light_filtered.csv",
    mime="text/csv"
)


# ==========================================================
# FOOTER
# ==========================================================

st.markdown(
    '<p class="footer-text">'
    'Smart Street Lighting Energy Optimization System '
    '| Big Data Analytics Project'
    '</p>',
    unsafe_allow_html=True
)
