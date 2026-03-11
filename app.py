import streamlit as st
import pandas as pd
import hashlib
import time
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import numpy as np
import random
import os

st.set_page_config(page_title="SmartVote Pro", layout="wide")

# -----------------------
# DARK UI
# -----------------------
st.markdown("""
<style>
.stApp {background-color:#0f0f0f;color:#f5f5f5;}
[data-testid="stSidebar"]{background-color:#1c1c1c;}
h1,h2,h3{color:white;}
.stButton>button{
background-color:#2f2f2f;
color:white;
border-radius:10px;
border:none;
padding:8px 20px;
}
.stButton>button:hover{background-color:#505050;}
[data-testid="metric-container"]{
background-color:#1f1f1f;
border-radius:12px;
padding:15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# DATASET GENERATION
# -----------------------
DATA_FILE = "dataset.csv"
regions_master = ["Tamil Nadu","Karnataka","Kerala","Andhra Pradesh","Telangana","Maharashtra","Delhi","Gujarat","West Bengal","Uttar Pradesh","Rajasthan","Madhya Pradesh"]
candidates_master = ["Rajesh Kumar","Priya Sharma","Amit Singh","Sunita Reddy","Rahul Verma","Anjali Nair","Vikram Patel"]

if not os.path.exists(DATA_FILE):
    data = []
    start = int(time.time())
    for i in range(1000):
        voter = f"VOTER{i+1}"
        region = random.choice(regions_master)
        candidate = random.choice(candidates_master)
        timestamp = start + i
        data.append([voter, region, candidate, timestamp])
    df_gen = pd.DataFrame(data, columns=["voter_id","region","candidate","timestamp"])
    df_gen.to_csv(DATA_FILE,index=False)

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(DATA_FILE)
regions = sorted(df["region"].unique())
candidates = sorted(df["candidate"].unique())

# -----------------------
# BLOCKCHAIN
# -----------------------
if "blockchain" not in st.session_state:
    st.session_state.blockchain = []

def create_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def add_block(voter,region,candidate):
    index=len(st.session_state.blockchain)
    timestamp=str(time.time())
    data=f"{voter}{region}{candidate}{timestamp}"
    prev_hash=(st.session_state.blockchain[-1]["hash"] if st.session_state.blockchain else "0")
    block={"index":index,"voter":voter,"region":region,"candidate":candidate,"timestamp":timestamp,"prev_hash":prev_hash,"hash":create_hash(data+prev_hash)}
    st.session_state.blockchain.append(block)

# -----------------------
# SESSION STATE
# -----------------------
if 'role' not in st.session_state:
    st.session_state.role = None
if 'login_time' not in st.session_state:
    st.session_state.login_time = None
if 'login_success' not in st.session_state:
    st.session_state.login_success = False

# -----------------------
# LOGIN SIDEBAR
# -----------------------
role_option = st.sidebar.selectbox("Select Role", ["Voter", "Admin", "Security"])
password = st.sidebar.text_input("Enter Password", type="password")
login_clicked = st.sidebar.button("Login")

if login_clicked:
    if (role_option == "Voter" and password == "123") or \
       (role_option == "Admin" and password == "admin123") or \
       (role_option == "Security" and password == "secure123"):
        st.session_state.role = role_option
        st.session_state.login_time = time.time()
        st.session_state.login_success = True
    else:
        st.sidebar.error("Invalid password")

# Logout
if st.session_state.login_success:
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.session_state.login_time = None
        st.session_state.login_success = False

# -----------------------
# LOGIN CHECK
# -----------------------
if not st.session_state.login_success:
    st.warning("🔒 Please login from the sidebar to access the system modules.")
    st.stop()

# -----------------------
# EXTRA FEATURE: Top Candidate + Total Votes
# -----------------------
if not df.empty:
    top_candidate = df['candidate'].value_counts().idxmax()
    top_votes = df['candidate'].value_counts().max()
    total_votes = df.shape[0]
    st.sidebar.markdown(f"🏆 **Top Candidate:** {top_candidate} ({top_votes} votes)")
    st.sidebar.markdown(f"🗳 **Total Votes Cast:** {total_votes}")

# -----------------------
# MAIN APP AFTER LOGIN
# -----------------------
st.markdown("<h1 style='text-align:center;'>🗳 SmartVote Pro</h1>",unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:grey;'>Blockchain Based AI Fraud Detection Voting System</h4>",unsafe_allow_html=True)
st.markdown("---")
st.sidebar.markdown(f"**Current Role:** {st.session_state.role}")

# -----------------------
# SESSION TIMER
# -----------------------
if st.session_state.login_time is not None:
    elapsed = int(time.time() - st.session_state.login_time)
    minutes, seconds = divmod(elapsed, 60)
    st.sidebar.markdown(f"**Session Duration:** {minutes}m {seconds}s")

# -----------------------
# SIDEBAR NAVIGATION
# -----------------------
menu_items = []
role = st.session_state.role
if role == "Voter":
    menu_items = ["⭐ Voting Portal", "⭐ Verify Vote"]
elif role == "Admin":
    menu_items = ["⭐ Election Dashboard", "⭐ Data Explorer"]
elif role == "Security":
    menu_items = ["⭐ Fraud Detection", "⭐ Blockchain Explorer"]

menu = st.sidebar.radio("Select Module", menu_items)

# -----------------------
# MODULES
# -----------------------

# VOTING PORTAL
if menu == "⭐ Voting Portal":
    st.header("🗳 Cast Your Vote")
    voter = st.text_input("Enter Voter ID")
    region = st.selectbox("Select Region", regions)
    candidate = st.selectbox("Select Candidate", candidates)
    if st.button("Submit Vote"):
        if voter != "":
            new_vote = {"voter_id": voter,"region": region,"candidate": candidate,"timestamp": int(time.time())}
            df.loc[len(df)] = new_vote
            df.to_csv(DATA_FILE,index=False)
            add_block(voter,region,candidate)
            st.success("Vote recorded and secured in blockchain")
        else:
            st.warning("Enter voter id")

# VERIFY VOTE
if menu == "⭐ Verify Vote":
    st.header("✅ Verify Your Vote")
    voter_id_input = st.text_input("Enter your Voter ID to verify")
    if st.button("Verify Vote"):
        votes = df[df["voter_id"] == voter_id_input]
        if not votes.empty:
            st.success("Vote Found!")
            st.dataframe(votes)
        else:
            st.error("No vote found for this Voter ID.")

# ELECTION DASHBOARD (Admin) + Pie Chart
if menu == "⭐ Election Dashboard":
    st.header("📊 Election Dashboard")
    for candidate in candidates:
        count = df[df["candidate"] == candidate].shape[0]
        st.metric(label=candidate, value=count)
    st.bar_chart(df['candidate'].value_counts())
    
    # Pie chart
    st.subheader("📈 Vote Distribution (Pie Chart)")
    pie_data = df['candidate'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

# DATA EXPLORER (Admin)
if menu == "⭐ Data Explorer":
    st.header("📂 Explore Voting Data")
    st.dataframe(df)

# FRAUD DETECTION (Security) + Anomaly % panel
if menu == "⭐ Fraud Detection":
    st.header("🚨 Fraud Detection")
    st.write("Detecting anomalies using Isolation Forest")
    iso = IsolationForest(contamination=0.05)
    if not df.empty:
        df_numeric = df.copy()
        df_numeric["timestamp"] = pd.to_numeric(df_numeric["timestamp"])
        preds = iso.fit_predict(df_numeric[["timestamp"]])
        df_numeric["fraud_flag"] = preds
        anomalies = df_numeric[df_numeric["fraud_flag"] == -1].shape[0]
        total = df_numeric.shape[0]
        st.metric(label="Total Records", value=total)
        st.metric(label="Anomalies Detected", value=anomalies)
        st.metric(label="Anomaly %", value=f"{round((anomalies/total)*100,2)}%")
        st.dataframe(df_numeric[df_numeric["fraud_flag"] == -1])

# BLOCKCHAIN EXPLORER (Security)
if menu == "⭐ Blockchain Explorer":
    st.header("⛓ Blockchain Explorer")
    if st.session_state.blockchain:
        st.dataframe(pd.DataFrame(st.session_state.blockchain))
    else:
        st.info("No blocks in blockchain yet.")
