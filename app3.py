import streamlit as st
import pandas as pd
import random

st.title("Clinical Trial Randomization Tool (Block Randomization)")
st.markdown("""
This tool performs a two-step randomization:
1. Stratify participants based on Sleep Quality (Good/Poor) and Sex (M/F)
2. Randomize within each stratum to Intervention (A) or Sham (B), using fixed-size blocks of 4 (e.g., AABB, ABAB)
""")

# Step 1: Stratification Inputs
st.header("Step 1: Stratification")
sleep_groups = ["Good", "Poor"]
sex_groups = ["M", "F"]

strata = [(sleep, sex) for sleep in sleep_groups for sex in sex_groups]

stratum_sizes = {}
for sleep, sex in strata:
    key = f"{sleep}_{sex}"
    n = st.number_input(f"Number of participants in {sleep} sleepers ({sex}) [must be multiple of 4]", min_value=0, value=0, step=4)
    stratum_sizes[key] = n

# Step 2: Randomization Inputs
st.header("Step 2: Randomization to A (Intervention) or B (Sham) in Blocks of 4")
initial_id = st.number_input("Initial subject ID", min_value=1, value=1, step=1)

if st.button("Generate Randomization Plan"):
    assignments = []
    subject_id = initial_id

    for key, n in stratum_sizes.items():
        sleep, sex = key.split("_")
        if n % 4 != 0:
            st.error(f"Number of participants in {key} must be divisible by 4.")
            continue

        num_blocks = n // 4
        block_template = ["A", "A", "B", "B"]

        all_labels = []
        for _ in range(num_blocks):
            block = block_template[:]
            random.shuffle(block)
            all_labels.extend(block)

        for label in all_labels:
            assignments.append({
                "Subject ID": subject_id,
                "Sleep Quality": sleep,
                "Sex": sex,
                "Condition": label
            })
            subject_id += 1

    df = pd.DataFrame(assignments)
    st.success("Randomization complete using block randomization!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="randomization_plan_blocks.csv")