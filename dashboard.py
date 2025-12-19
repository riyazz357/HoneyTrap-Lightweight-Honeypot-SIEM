import streamlit as st
import sqlite3
import pandas as pd
import requests
import time

st.set_page_config(page_title="HoneyTrap SIEM", page_icon="🛡️", layout="wide")
st.title("🛡️ HoneyTrap SIEM: Global Threat Map")

# --- 1. Data Fetching ---
def load_data():
    conn = sqlite3.connect('attacks.db')
    df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
    conn.close()
    return df

# --- 2. Geolocation Function (The Magic) ---
# We cache this so we don't spam the API for the same IP twice
@st.cache_data
def get_location(ip):
    if ip == "127.0.0.1" or ip == "localhost":
        return None, None
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response['status'] == 'success':
            return response['lat'], response['lon']
    except:
        pass
    return None, None

df = load_data()

if not df.empty:
    # --- 3. Process Map Data ---
    # Get unique IPs to avoid looking up the same one 50 times
    unique_ips = df['ip'].unique()
    
    # Create a list of locations
    map_data = []
    for ip in unique_ips:
        lat, lon = get_location(ip)
        if lat:
            map_data.append({'lat': lat, 'lon': lon})
    
    map_df = pd.DataFrame(map_data)

    # --- 4. The Dashboard Layout ---
    
    # ROW 1: THE MAP
    st.subheader("🗺️ Live Attack Origins")
    if not map_df.empty:
        st.map(map_df, zoom=1)
    else:
        st.info("No external IPs detected yet (Localhost doesn't show on map).")

    st.markdown("---")

    # ROW 2: METRICS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Attacks", len(df))
    c2.metric("Unique Attackers", df['ip'].nunique())
    c3.metric("SQL Injection", len(df[df['attack_type'] == 'SQL_INJECTION']) if 'attack_type' in df.columns else 0)
    
    # ROW 3: CHARTS
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🚨 Attack Types")
        if 'attack_type' in df.columns:
            st.bar_chart(df['attack_type'].value_counts())
    
    with col2:
        st.subheader("🌐 Top Attacking IPs")
        st.bar_chart(df['ip'].value_counts().head(5))

    # ROW 4: LOGS
    st.subheader("📝 Intrusion Logs")
    st.dataframe(df[['timestamp', 'ip', 'attack_type', 'payload']], use_container_width=True)

    if st.button('Refresh Data'):
        st.rerun()