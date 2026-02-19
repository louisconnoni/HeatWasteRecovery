




def read_key_value_file(file):
    data = {}
    lines = file.read().decode("utf-8").splitlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        key, value = line.split("=")
        key = key.strip()
        value = value.strip()

        try:
            value = float(value)
        except:
            pass

        data[key] = value

    return data

import streamlit as st

st.title("Data Center Sustainability Calculator")

metrics_file = st.file_uploader("Upload Metrics File", type="txt")
rules_file = st.file_uploader("Upload Rules File", type="txt")

if metrics_file and rules_file:

    metrics = read_key_value_file(metrics_file)
    rules = read_key_value_file(rules_file)

    st.write("Metrics:", metrics)
    st.write("Rules:", rules)


def score_metric(value, best, worst):
    if value >= worst:
        return 0
    if value <= best:
        return 100
    return 100 * (worst - value) / (worst - best)



cue_score = score_metric(metrics["CUE"], 0.2, 1.2)
pue_score = score_metric(metrics["PUE"], 1.1, 2.0)
wue_score = score_metric(metrics["WUE"], 0.1, 1.5)

final_score = (
    cue_score * rules["weight_CUE"] +
    pue_score * rules["weight_PUE"] +
    wue_score * rules["weight_WUE"]
)


st.subheader(f"Final Sustainability Score: {final_score:.2f}/100")


if final_score >= rules["excellent"]:
    category = "excellent"
elif final_score >= rules["good"]:
    category = "good"
elif final_score >= rules["acceptable"]:
    category = "acceptable"
else:
    category = "poor"


location = rules[f"{category}_location"]
recovery = rules[f"{category}_recovery"]

st.subheader("Recommendation")
st.write("Location Type:", location)
st.write("Heat Recovery Method:", recovery)