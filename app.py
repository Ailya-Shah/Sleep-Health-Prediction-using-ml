import streamlit as st

st.set_page_config(page_title="Sleep Quality Estimator", page_icon="🛌", layout="centered")

st.title("Sleep Quality Predictor (Quick Rough Estimate)")
st.caption("Dropdown-based estimate from sleep and lifestyle factors. Output: Good or Bad sleep quality.")

st.subheader("Select Features")

sleep_duration_band = st.selectbox(
    "Sleep Duration (hours)",
    [
        "Less than 5",
        "5 to 6.5",
        "6.5 to 8",
        "More than 8",
    ],
)

stress_level = st.selectbox(
    "Stress Score",
    [
        "Low (1-4)",
        "Moderate (5-7)",
        "High (8-10)",
    ],
)

sleep_latency_band = st.selectbox(
    "Sleep Latency (minutes to fall asleep)",
    [
        "0 to 15",
        "16 to 30",
        "More than 30",
    ],
)

wake_episodes_band = st.selectbox(
    "Night Wake Episodes",
    [
        "0 to 1",
        "2 to 3",
        "4 or more",
    ],
)

caffeine_band = st.selectbox(
    "Caffeine Before Bed (mg)",
    [
        "0",
        "1 to 100",
        "More than 100",
    ],
)

screen_time_band = st.selectbox(
    "Screen Time Before Bed (minutes)",
    [
        "0 to 30",
        "31 to 60",
        "More than 60",
    ],
)

alcohol_band = st.selectbox(
    "Alcohol Units Before Bed",
    [
        "0",
        "1 to 2",
        "More than 2",
    ],
)

exercise_day = st.selectbox("Exercised Today", ["No", "Yes"])


def estimate_sleep_quality() -> tuple[str, float, list[str]]:
    score = 0
    reasons = []

    if sleep_duration_band == "Less than 5":
        score -= 3
        reasons.append("Very short sleep duration")
    elif sleep_duration_band == "5 to 6.5":
        score -= 1
        reasons.append("Below ideal sleep duration")
    elif sleep_duration_band == "6.5 to 8":
        score += 2
        reasons.append("Healthy sleep duration range")
    else:
        score += 1
        reasons.append("Long sleep duration")

    if stress_level == "Low (1-4)":
        score += 2
        reasons.append("Low stress")
    elif stress_level == "Moderate (5-7)":
        score += 0
        reasons.append("Moderate stress")
    else:
        score -= 2
        reasons.append("High stress")

    if sleep_latency_band == "0 to 15":
        score += 2
        reasons.append("Falls asleep quickly")
    elif sleep_latency_band == "16 to 30":
        score += 0
    else:
        score -= 2
        reasons.append("Long sleep latency")

    if wake_episodes_band == "0 to 1":
        score += 2
        reasons.append("Low sleep interruption")
    elif wake_episodes_band == "2 to 3":
        score += 0
    else:
        score -= 2
        reasons.append("Frequent night awakenings")

    if caffeine_band == "0":
        score += 1
    elif caffeine_band == "1 to 100":
        score += 0
    else:
        score -= 2
        reasons.append("High late caffeine intake")

    if screen_time_band == "0 to 30":
        score += 1
    elif screen_time_band == "31 to 60":
        score += 0
    else:
        score -= 1
        reasons.append("High pre-bed screen exposure")

    if alcohol_band == "0":
        score += 1
    elif alcohol_band == "1 to 2":
        score += 0
    else:
        score -= 1
        reasons.append("High alcohol intake before sleep")

    if exercise_day == "Yes":
        score += 1
        reasons.append("Physical activity present")
    else:
        score -= 0

    # Convert rough score to a pseudo-probability for user feedback.
    max_score = 12
    min_score = -12
    normalized = (score - min_score) / (max_score - min_score)
    probability_good = max(0.0, min(1.0, normalized))

    label = "Good" if score >= 2 else "Bad"
    return label, probability_good, reasons


if st.button("Predict Sleep Quality", type="primary"):
    label, prob_good, reasons = estimate_sleep_quality()

    if label == "Good":
        st.success(f"Predicted Sleep Quality: {label}")
    else:
        st.error(f"Predicted Sleep Quality: {label}")

    st.metric("Estimated probability of Good sleep", f"{prob_good * 100:.1f}%")

    with st.expander("Why this estimate?", expanded=True):
        for reason in reasons:
            st.write(f"- {reason}")

st.markdown("---")
st.caption(
    "Note: This is a rule-based rough estimator for quick project demo use. "
    "For production, use your trained ML pipeline and calibration."
)
