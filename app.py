import streamlit as st
import numpy as np
from statistics import stdev
from scipy.stats import t

# Function (fixed version)
def one_t(pop_mean, x, alternative):
    n1 = len(x)
    xbar = np.mean(x)
    sd = stdev(x)
    df = n1 - 1
    alpha = 0.05

    se = sd / np.sqrt(n1)
    t_cal = (xbar - pop_mean) / se

    if alternative == "greater":
        critical = t.ppf(1 - alpha, df)
        decision = "Reject H0" if t_cal > critical else "Accept H0"

    elif alternative == "lesser":
        critical = t.ppf(alpha, df)
        decision = "Reject H0" if t_cal < critical else "Accept H0"

    elif alternative == "two":
        critical_pos = t.ppf(1 - alpha/2, df)
        critical_neg = t.ppf(alpha/2, df)
        decision = "Reject H0" if (t_cal > critical_pos or t_cal < critical_neg) else "Accept H0"

    return t_cal, decision


# ---------------- STREAMLIT FRONTEND ----------------

st.title("One Sample t-Test")

# Population mean input
pop_mean = st.number_input("Enter Population Mean")

# Dataset input (comma separated)
data_input = st.text_input("Enter Dataset (comma separated values)",
                           "10,12,9,11,13")

# Alternative hypothesis selector
alternative = st.selectbox(
    "Select Alternative Hypothesis",
    ["greater", "lesser", "two"]
)

if st.button("Run Test"):
    try:
        # Convert string input to list
        x = list(map(float, data_input.split(",")))

        t_value, result = one_t(pop_mean, x, alternative)

        st.write(f"### t-value: {round(t_value, 4)}")
        st.success(f"Decision: {result}")

    except:
        st.error("Please enter valid numeric dataset!")