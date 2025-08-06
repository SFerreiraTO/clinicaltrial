import streamlit as st
import pandas as pd
import random

st.title("Clinical Trial Randomization Tool")
st.markdown("""
This tool performs a two-step randomization:
1. Stratify participants based on Sleep Quality (Good/Poor) and Sex (M/F)
2. Randomize within each stratum to Intervention (A) or Sham (B)
""")

# Step 1: Stratification Inputs
st.header("Step 1: Stratification")
sleep_groups = ["Good", "Poor"]
sex_groups = ["M", "F"]

strata = [(sleep, sex) for sleep in sleep_groups for sex in sex_groups]

stratum_sizes = {}
for sleep, sex in strata:
    key = f"{sleep}_{sex}"
    n = st.number_input(f"Number of participants in {sleep} sleepers ({sex})", min_value=0, value=0, step=1)
    stratum_sizes[key] = n

# Step 2: Randomization Inputs
st.header("Step 2: Randomization to A (Intervention) or B (Sham)")
initial_id = st.number_input("Initial subject ID", min_value=1, value=1, step=1)

if st.button("Generate Randomization Plan"):
    assignments = []
    subject_id = initial_id

    for key, n in stratum_sizes.items():
        sleep, sex = key.split("_")
        group_labels = ["A", "B"] * (n // 2)
        remainder = n % 2
        if remainder:
            group_labels.append(random.choice(["A", "B"]))
        random.shuffle(group_labels)

        for label in group_labels:
            assignments.append({
                "Subject ID": subject_id,
                "Sleep Quality": sleep,
                "Sex": sex,
                "Condition": label
            })
            subject_id += 1

    df = pd.DataFrame(assignments)
    st.success("Randomization complete!")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="randomization_plan.csv")