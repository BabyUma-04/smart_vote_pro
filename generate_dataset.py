import pandas as pd
import random
import time

# ------------------------------------------------
# INDIAN STATES / REGIONS
# ------------------------------------------------

regions = [
"Tamil Nadu",
"Karnataka",
"Kerala",
"Andhra Pradesh",
"Telangana",
"Maharashtra",
"Delhi",
"Gujarat",
"West Bengal",
"Uttar Pradesh",
"Rajasthan",
"Madhya Pradesh"
]

# ------------------------------------------------
# INDIAN CANDIDATE NAMES
# ------------------------------------------------

candidates = [
"Rajesh Kumar",
"Priya Sharma",
"Amit Singh",
"Sunita Reddy",
"Rahul Verma",
"Anjali Nair",
"Vikram Patel"
]

# ------------------------------------------------
# GENERATE DATASET
# ------------------------------------------------

data = []

start_time = int(time.time())

for i in range(1000):

    voter_id = f"VOTER{i+1}"

    region = random.choice(regions)

    candidate = random.choice(candidates)

    timestamp = start_time + i

    data.append([voter_id, region, candidate, timestamp])

# ------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------

df = pd.DataFrame(
data,
columns=["voter_id", "region", "candidate", "timestamp"]
)

# ------------------------------------------------
# SAVE DATASET
# ------------------------------------------------

df.to_csv("dataset.csv", index=False)

print("✅ Indian election dataset generated successfully!")
print("Total votes generated:", len(df))