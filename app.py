"""
AeroDash simple app
run with: streamlit run app.py
"""

import os
import streamlit as st
import pandas as pd
from data_fetcher import fetch_states, fetch_weather
from utils import format_aircraft_row

st.set_page_config(page_title="AeroDash", layout="wide")
st.title("AeroDash — Simple Demo")

st.sidebar.header("Controls")
use_sample = st.sidebar.checkbox("Use sample data", value=True)
bbox = st.sidebar.text_input("Bounding box", "20.5,72.5,28.9,77.5")
min_alt = st.sidebar.number_input("Min altitude (m)", value=0)
max_alt = st.sidebar.number_input("Max altitude (m)", value=15000)
refresh_sec = st.sidebar.slider("Auto-refresh (s)", 0, 60, 0)

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

def load_data(bbox_str, use_sample_flag):
    states = fetch_states(bbox=bbox_str, use_sample=use_sample_flag)
    if not states:
        return pd.DataFrame()
    rows = [format_aircraft_row(s) for s in states]
    df = pd.DataFrame(rows)
    df = df.dropna(subset=["lat", "lon"])
    df["alt_m"] = pd.to_numeric(df["alt_m"], errors="coerce")
    df = df[(df["alt_m"] >= min_alt) & (df["alt_m"] <= max_alt)]
    return df

if st.sidebar.button("Fetch now"):
    st.session_state.df = load_data(bbox, use_sample)
    st.success(f"Loaded {len(st.session_state.df)} rows")

if refresh_sec > 0:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=refresh_sec * 1000, key="auto")

col_map, col_table = st.columns([1.6, 1])

if st.session_state.df.empty:
    st.info("No data. Click Fetch now or enable sample data.")
else:
    df = st.session_state.df.copy()
    with col_table:
        st.subheader(f"Table ({len(df)})")
        show = df[["icao24", "callsign", "alt_m", "velocity", "origin_country", "lat", "lon"]].fillna("")
        show = show.rename(columns={
            "icao24": "ICAO24",
            "callsign": "Callsign",
            "alt_m": "Altitude (m)",
            "velocity": "Speed",
            "origin_country": "Origin",
            "lat": "Lat",
            "lon": "Lon"
        })
        st.dataframe(show, height=600)
        choice = st.selectbox("Pick ICAO24", options=df["icao24"].tolist())
        if st.button("Weather for picked"):
            sel = df[df["icao24"] == choice].iloc[0]
            w = fetch_weather(sel["lat"], sel["lon"])
            st.write(w)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, file_name="aerodash.csv")

    with col_map:
        st.subheader("Map")
        map_df = df.rename(columns={"lat": "lat", "lon": "lon"})
        st.map(map_df[["lat", "lon"]], zoom=6)
        st.write("Stats")
        c1, c2, c3 = st.columns(3)
        c1.metric("Aircraft", len(df))
        avg_alt = int(df["alt_m"].mean()) if not df["alt_m"].isnull().all() else 0
        c2.metric("Avg alt (m)", f"{avg_alt}")
        avg_speed = int(pd.to_numeric(df["velocity"], errors="coerce").mean() or 0)
        c3.metric("Avg speed", f"{avg_speed}")

if st.session_state.df.empty and use_sample:
    if st.button("Load demo sample"):
        st.session_state.df = load_data(bbox, True)
        st.rerun()
