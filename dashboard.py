import streamlit as st
import sqlite3
import pandas as pd
import time

# --- Page Config ---
st.set_page_config(
    page_title="HoneyTrap SIEM",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ HoneyTrap SIEM: Live Threat Intelligence")

# --- 1. Data Fetching Function ---
def load_data():
    try:
        # Connect to the database created by app.py
        conn = sqlite3.connect('attacks.db')
        query = "SELECT * FROM logs ORDER BY id DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return pd.DataFrame()

# --- 2. Load Data ---
df = load_data()

if df.empty:
    st.warning("No attacks detected yet. Waiting for traffic...")
    st.info("Run 'python app.py' and try logging in at localhost:5000/admin")
else:
    # --- Data Processing (Extracting Username from Payload) ---
    # The payload looks like: "User: admin | Pass: 123"
    # We want just "admin" for our charts.
    try:
        df['username_attempted'] = df['payload'].apply(lambda x: x.split('|')[0].replace('User: ', '').strip())
    except:
        df['username_attempted'] = "Unknown"

    # --- 3. Key Metrics (KPIs) ---
    # Create 3 columns for top-level stats
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total Attacks Captured", value=len(df))
    
    with col2:
        unique_ips = df['ip'].nunique()
        st.metric(label="Unique Attackers (IPs)", value=unique_ips)
    
    with col3:
        # Show the most recent attack time
        last_attack = df['timestamp'].iloc[0]
        st.metric(label="Last Incident", value=last_attack.split(' ')[1]) # Just show time

    st.markdown("---")

    # --- 4. Visualizations ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("🚨 Top Targeted Usernames")
        # Count how many times each username was tried
        username_counts = df['username_attempted'].value_counts().head(5)
        st.bar_chart(username_counts)

    with col_chart2:
        st.subheader("🌐 Top Attacking IPs")
        ip_counts = df['ip'].value_counts().head(5)
        st.bar_chart(ip_counts)

    # --- 5. Raw Evidence Log ---
    st.subheader("📝 Live Intrusion Logs")
    
    # We create a cleaner view for the table
    display_df = df[['timestamp', 'ip', 'payload','attack_type' ,'user_agent']]
    st.dataframe(display_df, use_container_width=True)

    # --- Auto-Refresh Button ---
    if st.button('Refresh Data'):
        st.rerun()