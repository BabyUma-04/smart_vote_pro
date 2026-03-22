import streamlit as st
import pandas as pd
import hashlib
import time
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import numpy as np
import random
import os



#  page title and icon


st.set_page_config(
    page_title="Secure-Vote",  
    page_icon="🗳️",           
    layout="wide"              
)


# -----------------------
# MODERN CSS
# -----------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Navbar */
.logo {
    font-size:22px;
    font-weight:bold;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    padding:25px;
    border-radius:20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    margin-bottom:20px;
    transition:0.3s;
}
.card:hover {
    transform: translateY(-5px);
}

/* Center Box */
.center-box {
    width:350px;
    margin:auto;
    margin-top:100px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(45deg,#ff512f,#dd2476);
    color:white;
    border-radius:25px;
    padding:10px;
    border:none;
    width:100%;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* Footer */
.footer {
    text-align:center;
    padding:20px;
    color:lightgray;
}

</style>
""", unsafe_allow_html=True)





menu = ["🏠 Home", "🔐 Login", "🗳 Vote", "⚙ Admin", "Security"]

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

choice = st.selectbox("Navigation", menu, index=menu.index(st.session_state.page))





# -----------------------
# DATASET GENERATION
# -----------------------
DATA_FILE = "dataset.csv"
regions_master="TamilNadu"
parties_master = ["BMK","ABBMK","KMNK","TMK","BVK","AMVK","BJMK"]

if not os.path.exists(DATA_FILE):
    data = []
    start = int(time.time())
    for i in range(1000):
        voter = f"VOTER{i+1}"
        region = "TamilNadu"
        party = random.choice(parties_master)
        timestamp = start + i
        data.append([voter, region, party, timestamp])
    df_gen = pd.DataFrame(data, columns=["voter_id","region","party","timestamp"])
    df_gen.to_csv(DATA_FILE,index=False)



# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(DATA_FILE)
party = sorted([p for p in df["party"].unique() if isinstance(p, str)])

# -----------------------
# BLOCKCHAIN
# -----------------------

if "blockchain" not in st.session_state:
    st.session_state.blockchain = []

def create_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def add_block(voter, party):
    index = len(st.session_state.blockchain)
    timestamp = str(time.time())

    data = f"{voter}|TamilNadu|{party}|{timestamp}"
    prev_hash = st.session_state.blockchain[-1]["hash"] if index > 0 else "0"

    block = {
        "index": index,
        "voter": voter,
        "state": "Tamil Nadu",
        "party": party,
        "timestamp": timestamp,
        "prev_hash": prev_hash,
        "hash": create_hash(data + prev_hash)
    }

    st.session_state.blockchain.append(block)

    def validate_chain():
        for i in range(1, len(block)):
            if block[i]["prev_hash"] != block[i-1]["hash"]:
                return False
        return True





# -----------------------
# ADDING DATASET TO THE BLOCKS
# -----------------------


def add_dataset_to_blockchain(df):
    if len(st.session_state.blockchain) == 0:  # Only once

        for i, row in df.iterrows():
            index = len(st.session_state.blockchain)

            data = f"{row['voter_id']}|{row['region']}|{row['party']}|{row['timestamp']}"
            prev_hash = st.session_state.blockchain[-1]["hash"] if index > 0 else "0"

            block = {
                "index": index,
                "voter": row["voter_id"],
                "state": row["region"],
                "party": row["party"],
                "timestamp": str(row["timestamp"]),
                "prev_hash": prev_hash,
                "hash": create_hash(data + prev_hash)
            }

            st.session_state.blockchain.append(block)



# -----------------------
# CALLING THE FUNCTION
# -----------------------


df = pd.read_csv(DATA_FILE)

add_dataset_to_blockchain(df)   # 🔥

# -----------------------
# VALIDATE BLOCKCHAIN
# -----------------------

def validate_chain():
    chain = st.session_state.blockchain
    for i in range(1, len(chain)):
        if chain[i]["prev_hash"] != chain[i-1]["hash"]:
            return False
    return True



# -----------------------
# SESSION STATE
# -----------------------
if 'role' not in st.session_state:
    st.session_state.role = None
if 'login_time' not in st.session_state:
    st.session_state.login_time = None
if 'login_success' not in st.session_state:
    st.session_state.login_success = False



if choice == "🏠 Home":
    st.markdown("""
    <div class="card">
        <h1>🗳 SmartVote System</h1>
        <p>Secure Blockchain Voting with AI Fraud Detection</p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.role = None   
    st.session_state.sidebar_menu = None  
    col1, col2, col3 = st.columns(3)

    col1.markdown('<div class="card">🔐 Secure Voting</div>', unsafe_allow_html=True)
    col2.markdown('<div class="card">🤖 AI Fraud Detection</div>', unsafe_allow_html=True)
    col3.markdown('<div class="card">📊 Live Dashboard</div>', unsafe_allow_html=True)


    page = st.sidebar.selectbox("Navigation", ["Home", "Voting", "Admin"])

    if choice == "🏠 Home":
        st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True
        )



# -----------------------
# LOGIN SIDEBAR
# -----------------------

elif choice == "🔐 Login":


    st.markdown("""
    <div style="
    padding:15px;
    border-radius:10px;
    text-align:center;
    color:black;
    width:350px;
    margin:auto;
    ">
    <h3 style="margin:5px;">🔐 SmartVote Login</h3>
    <p style="margin:0; font-size:14px;">Secure Voting System</p>
    </div>
    """, unsafe_allow_html=True)

    if choice == "🔐 Login":
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"] {display: none;}
            </style>
            """,
            unsafe_allow_html=True
            )


    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("### 👤 Login")

        role_option = st.selectbox("Select Role", ["Voter", "Admin", "Security"])
        st.session_state.page = choice
        password = st.text_input("Enter Password", type="password")

        login_clicked = st.button("🚀 Login")

    


    role_icons = {
        "Voter": "🧑‍💼",
        "Admin": "👨‍💻",
        "Security": "🛡"
    }

    st.markdown(f"### {role_icons[role_option]} {role_option} Login")


    if login_clicked:
        if (role_option == "Voter" and password == "123") or \
            (role_option == "Admin" and password == "admin123") or \
            (role_option == "Security" and password == "secure123"):

            st.success("✅ Login Successful!")
            st.session_state.role = role_option
            st.session_state.login_time = time.time()
            st.session_state.login_success = True

            # 🔥 REDIRECT LOGIC
            if role_option == "Admin":
                st.session_state.page = "⚙ Admin"
            elif role_option == "Voter":
                st.session_state.page = "🗳 Vote"
            elif role_option == "Security":
                st.session_state.page = "Security"
            st.rerun()
        else :
            st.error("X Invalid Password")
        
    


elif choice == "🗳 Vote":

    if st.session_state.login_success:

        st.markdown('<div class="card"><h4>🗳 Vote Now</h4></div>', unsafe_allow_html=True)

    


# Logout
if st.session_state.login_success:
    if st.sidebar.button("Logout"):
        st.session_state.role = None
        st.session_state.login_time = None
        st.session_state.login_success = False

# -----------------------
# LOGIN CHECK
# -----------------------


# -----------------------
# EXTRA FEATURE: Top Candidate + Total Votes
# -----------------------
if not df.empty:
    top_candidate = df['party'].value_counts().idxmax()
    top_votes = df['party'].value_counts().max()
    total_votes = df.shape[0]
    st.sidebar.markdown(f"🏆 **Top Candidate:** {top_candidate} ({top_votes} votes)")
    st.sidebar.markdown(f"🗳 **Total Votes Cast:** {total_votes}")

# -----------------------
# MAIN APP AFTER LOGIN
# -----------------------


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

if "sidebar_menu" not in st.session_state:
    st.session_state.sidebar_menu = menu_items[0] if menu_items else None

menu = st.sidebar.radio(
    "Select Module",
    menu_items,
    key="sidebar_menu"
)

# -----------------------
# MODULES
# -----------------------

# VOTING PORTAL


if choice == "🗳 Vote" and menu == "⭐ Voting Portal":

    import re

    st.markdown("""
    <style>
    .vote-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="vote-card">', unsafe_allow_html=True)
    st.markdown("## 🗳 Secure Voting Portal")

    # -----------------------
    # 🧠 SESSION INIT
    # -----------------------
    if "otp" not in st.session_state:
        st.session_state.otp = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "verified_voter" not in st.session_state:
        st.session_state.verified_voter = None

    # -----------------------
    # 👤 INPUT VOTER ID
    # -----------------------
    voter_id = st.text_input("Enter Voter ID (Example: VOTER123)")

    # -----------------------
    # 🔍 VALIDATION FUNCTION
    # -----------------------
    def is_valid_voter(voter):
        if voter.strip() == "":
            return "⚠ Enter Voter ID"

        if not re.match(r"^VOTER\d+$", voter):
            return "❌ Invalid format! Use VOTER123"

        if len(voter) < 6 or len(voter) > 12:
            return "❌ Voter ID must be 6–12 characters"

        return "valid"

    # -----------------------
    # 🔐 VERIFY VOTER
    # -----------------------
    if st.button("🔍 Verify Voter"):

        voter_id = voter_id.strip()
        validation = is_valid_voter(voter_id)

        if validation != "valid":
            st.error(validation)


        # ✅ NEW: duplicate check using dataset
        elif voter_id in df["voter_id"].values:
            st.error("❌ You have already voted!")

        else:
            otp = str(random.randint(1000, 9999))
            st.session_state.otp = otp
            st.session_state.verified_voter = voter_id

            st.success(f"✅ OTP Sent (Demo): {otp}")

    # -----------------------
    # 🔢 OTP VERIFICATION
    # -----------------------
    if st.session_state.otp:

        user_otp = st.text_input("Enter OTP")

        if st.button("✅ Verify OTP"):

            if user_otp == st.session_state.otp:
                st.success("✅ OTP Verified Successfully!")
                st.session_state.authenticated = True
            else:
                st.error("❌ Invalid OTP")

    # -----------------------
    # 🗳 CAST VOTE
    # -----------------------
    if st.session_state.authenticated:

        st.markdown("### 🗳 Cast Your Vote")

        parties = st.selectbox("Choose Party", party)
        region = st.text_input("region", "Tamil Nadu")

        if st.button("🚀 Submit Vote"):

            voter_id = st.session_state.verified_voter

            new_vote = {
                "voter_id": voter_id,
                "region": "TamilNadu",
                "party": parties,
                "timestamp": int(time.time())
            }

            df.loc[len(df)] = new_vote

            # ✅ Correct saving
            df.to_csv(DATA_FILE, index=False)

            # 🔗 Add to blockchain
            add_block(voter_id, parties)

            st.success("🎉 Vote successfully secured in Blockchain!")

            # Reset session
            st.session_state.authenticated = False
            st.session_state.otp = None
            st.session_state.verified_voter = None

    st.markdown("</div>", unsafe_allow_html=True)

# VERIFY VOTE
if choice == "🗳 Vote" and menu == "⭐ Verify Vote":
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


elif choice == "⚙ Admin":
    

    if st.session_state.role != "Admin":
        st.error("⛔ Access Denied")
        st.stop()

    st.markdown('<div class="card"><h2>⚙ Admin Panel</h2></div>', unsafe_allow_html=True)

    st.write("Manage Users / Votes / System")


    if choice == "⚙ Admin" and menu == "⭐ Election Dashboard":
        st.markdown('<div class="card-custom">', unsafe_allow_html=True)
        st.header("📊 Election Dashboard")

        col1, col2, col3 = st.columns(3)

        total_votes = df.shape[0]
        top_candidate = df['party'].value_counts().idxmax()
        fraud_placeholder = "AI Active"

        col1.metric("Total Votes", total_votes)
        col2.metric("Top Candidate", top_candidate)
        col3.metric("System Status", fraud_placeholder)

        st.markdown("</div>", unsafe_allow_html=True)

        # Bar Chart
        st.markdown('<div class="card-custom">', unsafe_allow_html=True)
        st.subheader("📊 Vote Count")
        st.bar_chart(df['party'].value_counts())
        st.markdown("</div>", unsafe_allow_html=True)

    # DATA EXPLORER (Admin)
    if choice == "⚙ Admin" and menu == "⭐ Data Explorer":
        st.header("📂 Explore Voting Data")
        st.dataframe(df)

# FRAUD DETECTION (Security) + Anomaly % panel
elif choice == "Security":
    if st.session_state.role != "Security":
        st.error("⛔ Access Denied")
        st.stop()
if choice == "Security" and menu == "⭐ Fraud Detection":
    st.markdown('<div class="card-custom">', unsafe_allow_html=True)
    st.header("🚨 Fraud Detection System")

    iso = IsolationForest(contamination=0.05)

    if not df.empty:
        df_numeric = df.copy()
        df_numeric["timestamp"] = pd.to_numeric(df_numeric["timestamp"])

        preds = iso.fit_predict(df_numeric[["timestamp"]])
        df_numeric["fraud_flag"] = preds

        anomalies = df_numeric[df_numeric["fraud_flag"] == -1].shape[0]
        total = df_numeric.shape[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", total)
        col2.metric("Fraud Cases", anomalies)
        col3.metric("Fraud %", f"{round((anomalies/total)*100,2)}%")

        st.dataframe(df_numeric[df_numeric["fraud_flag"] == -1])

    st.markdown("</div>", unsafe_allow_html=True)


# BLOCKCHAIN EXPLORER (Security)
if choice == "Security" and menu == "⭐ Blockchain Explorer":

    # -----------------------
    # 🎨 ADVANCED UI CSS
    # -----------------------
    st.markdown("""
    <style>
    .block-card {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 18px;
        margin: 12px 0;
        border-left: 6px solid #00ffcc;
        box-shadow: 0 8px 25px rgba(0,0,0,0.6);
        transition: 0.3s;
    }
    .block-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 10px 35px rgba(0,255,204,0.3);
    }
    .block-tampered {
        border-left: 6px solid #ff4b4b !important;
        box-shadow: 0 10px 35px rgba(255,75,75,0.4);
    }
    .chain-arrow {
        text-align: center;
        font-size: 22px;
        color: #00ffcc;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------
    # 🧠 SESSION INIT
    # -----------------------
    if "search" not in st.session_state:
        st.session_state.search = ""

    def clear_search():
        st.session_state.search = ""

    chain = st.session_state.blockchain

    if not chain:
        st.info("No blocks available.")
        st.stop()

    # -----------------------
    # 🌟 TITLE
    # -----------------------
    st.markdown("""
    <h1 style='text-align:center;
    background: linear-gradient(90deg,#00ffcc,#00c3ff);
    -webkit-background-clip: text;
    color: transparent;'>
    ⛓ Smart Blockchain Explorer
    </h1>
    """, unsafe_allow_html=True)

    # -----------------------
    # 🔍 SEARCH + FILTER
    # -----------------------
    col1, col2, col3 = st.columns([3,1,1])

    with col1:
        search_query = st.text_input("🔍 Search (voter / hash / party / index)", key="search")

    with col2:
        party_filter = st.selectbox(
            "🎯 Party",
            ["All"] + list(set([b["party"] for b in chain]))
        )

    with col3:
        st.button("❌ Clear", on_click=clear_search)

    search_query = search_query.strip().lower()

    # -----------------------
    # 💡 SUGGESTIONS
    # -----------------------
    if search_query:
        suggestions = set()
        for b in chain:
            if search_query in b["voter"].lower():
                suggestions.add(b["voter"])
            if search_query in b["party"].lower():
                suggestions.add(b["party"])

        if suggestions:
            st.caption("💡 Suggestions:")
            st.write(", ".join(list(suggestions)[:5]))

    # -----------------------
    # 🔢 JUMP TO BLOCK
    # -----------------------
    jump_index = st.number_input("🔢 Jump to Block", min_value=0, step=1)

    if st.button("Go"):
        for b in chain:
            if b["index"] == jump_index:
                st.success(f"Jumped to Block {jump_index}")
                st.json(b)
                break

    # -----------------------
    # 🔎 FILTER LOGIC
    # -----------------------
    filtered_blocks = []

    for block in chain:

        if party_filter != "All" and block["party"] != party_filter:
            continue

        if search_query == "":
            filtered_blocks.append(block)
        else:
            if (
                search_query in str(block["voter"]).lower() or
                search_query in str(block["party"]).lower() or
                search_query in str(block["hash"]).lower() or
                search_query in str(block["prev_hash"]).lower() or
                search_query in str(block["index"])
            ):
                filtered_blocks.append(block)

    if not filtered_blocks:
        st.warning("No matching blocks found 🔎")
        st.stop()

    # -----------------------
    # 🔗 CHAIN VISUAL
    # -----------------------
    st.subheader("🔗 Chain Structure")

    chain_str = " → ".join([str(b["index"]) for b in filtered_blocks[:20]])
    st.markdown(f"""
    <div style="
        padding:12px;
        background: rgba(0,0,0,0.4);
        border-radius:10px;
        text-align:center;
    ">
        {chain_str} {"..." if len(filtered_blocks) > 20 else ""}
    </div>
    """, unsafe_allow_html=True)

    # -----------------------
    # 🎨 HIGHLIGHT
    # -----------------------
    def highlight(text):
        if not search_query:
            return text
        return str(text).replace(
            search_query,
            f"<span style='color:#00ffcc;font-weight:bold'>{search_query}</span>"
        )

    # -----------------------
    # 🧱 BLOCK DISPLAY
    # -----------------------
    for i, block in enumerate(filtered_blocks):

        tampered = False
        if block["index"] > 0:
            prev_block = chain[block["index"] - 1]
            if block["prev_hash"] != prev_block["hash"]:
                tampered = True

        card_class = "block-card block-tampered" if tampered else "block-card"

        st.markdown(f"""
        <div class="{card_class}">
        <h4>🧱 Block #{block['index']}</h4>

        <p><b>👤 Voter:</b> {highlight(block['voter'])}</p>
        <p><b>🗳 Party:</b> {highlight(block['party'])}</p>
        <p><b>🗺 State:</b> {block['state']}</p>
        <p><b>⏱ Timestamp:</b> {block['timestamp']}</p>

        <p><b>🔗 Prev Hash:</b><br>
        <span style="font-size:12px;color:#ccc; word-break:break-all;">
        {highlight(block['prev_hash'])}
        </span></p>

        <p><b>🔐 Hash:</b><br>
        <span style="font-size:12px;color:#00ffcc; word-break:break-all;">
        {highlight(block['hash'])}
        </span></p>

        </div>
        """, unsafe_allow_html=True)

        if i < len(filtered_blocks) - 1:
            st.markdown('<div class="chain-arrow">⬇️</div>', unsafe_allow_html=True)

        if tampered:
            st.error("⚠️ Block integrity broken!")

    # -----------------------
    # ✅ VALIDATION
    # -----------------------
    st.markdown("---")

    if validate_chain():
        st.success("✅ Blockchain is valid (No tampering detected)")
    else:
        st.error("❌ Blockchain compromised!")


st.markdown("""
            <div class = "footer"
            <div style="text-align:center; padding:20px; font-size:14px; color:gray;">
            🔐 Powered by Blockchain | 🤖 AI Secured | © 2026 SmartVote
            </div>
            """, unsafe_allow_html=True)
