import streamlit as st

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="🔥 ΔTc Calculator",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🔥 ΔT₍c₎ Calculator")
st.markdown("Calculate the contact temperature rise (ΔT) for polymer-steel contacts.")
st.markdown("**All inputs are in SI units.**")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Input Parameters")

# Friction and force: no limits
mu = st.sidebar.number_input("Friction coefficient μ [-]", value=0.1, step=0.01, format="%.3f")
Fn = st.sidebar.number_input("Normal force Fₙ [N]", value=100.0, step=1.0, format="%.2f")

# Geometry & velocity with limits (converted to meters from mm)
v = st.sidebar.number_input("Sliding velocity v [m/s]", min_value=0.25, max_value=1.0, value=0.25, step=0.01, format="%.3f")
r = st.sidebar.number_input("Sliding radius r [m]", min_value=0.009, max_value=0.019, value=0.009, step=0.001, format="%.4f")
r_d = st.sidebar.number_input("Steel disc radius r_d [m]", min_value=0.025, max_value=0.060, value=0.025, step=0.001, format="%.4f")
b = st.sidebar.number_input("Steel disc thickness b [m]", min_value=0.005, max_value=0.015, value=0.005, step=0.001, format="%.4f")
b_PTFE = st.sidebar.number_input("PTFE thickness b_PTFE [m]", min_value=0.005, max_value=0.015, value=0.005, step=0.001, format="%.4f")

# -----------------------------
# ΔT calculation
# -----------------------------
def calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE):
    return 0.11 * (mu * Fn) * v**0.71 * r**0.30 * r_d**(-1.70) * b**(-0.23) * b_PTFE**0.36

delta_Tc = calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE)

# -----------------------------
# Show result
# -----------------------------
st.subheader("Results")
st.write(f"**ΔT₍c₎ = {delta_Tc:.2f} °C**")

st.markdown("---")
st.markdown(
    "**Input Values Entered:**"
)
st.write(f"Friction μ = {mu}")
st.write(f"Normal force Fₙ = {Fn} N")
st.write(f"Sliding velocity v = {v} m/s")
st.write(f"Sliding radius r = {r} m")
st.write(f"Steel disc radius r_d = {r_d} m")
st.write(f"Steel disc thickness b = {b} m")
st.write(f"PTFE thickness b_PTFE = {b_PTFE} m")
































