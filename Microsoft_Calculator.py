import streamlit as st

import csv
import io
# -----------------------------
# Functions
# -----------------------------
def read_upfront_water_costs(file):
    costs = []

    file.seek(0)
    stringio = io.StringIO(file.getvalue().decode("utf-8"))
    reader = csv.reader(stringio)

    for row in reader:
        # skip empty rows
        if not row:
            continue

        # 6th column (index 5)
        cost = float(row[5])
        costs.append(cost)

    return costs


def score_metric(value, best, worst):
    if value >= worst:
        return 0
    if value <= best:
        return 100
    return 100 * (worst - value) / (worst - best)


# -----------------------------
# UI
# -----------------------------
st.title("Data Center Sustainability Calculator")

metrics_file = st.file_uploader("Upload Metrics CSV", type="csv")
rules_file = st.file_uploader("Upload Rules CSV", type="txt")

# -----------------------------
# Main Logic
# -----------------------------
if metrics_file is not None:

    costs = read_upfront_water_costs(metrics_file)

    st.write("Upfront Water Costs:", costs)

else:
    st.info("Please upload BOTH files to run the calculator.")