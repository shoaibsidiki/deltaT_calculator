import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ΔTc Full Map", layout="wide")
st.title("🔥 ΔT₍c₎ Full Temperature Map")

# -----------------------------
# Fixed Inputs
# -----------------------------
st.sidebar.header("Fixed Inputs")
mu = st.sidebar.number_input("Friction coefficient μ [-]", value=0.1, step=0.01)
Fn = st.sidebar.number_input("Normal force Fₙ [N]", value=100.0, step=1.0)

# -----------------------------
# Parameter Ranges
# -----------------------------
st.sidebar.header("Parameter Ranges for ΔT Map")
v_min, v_max = st.sidebar.slider("Sliding velocity v [m/s]", 0.25, 1.0, (0.25, 1.0), 0.01)
r_min, r_max = st.sidebar.slider("Sliding radius r [m]", 0.009, 0.019, (0.009, 0.019), 0.001)

# Fixed geometry values
r_d = st.sidebar.number_input("Steel disc radius r_d [m]", value=0.025, step=0.001)
b = st.sidebar.number_input("Steel disc thickness b [m]", value=0.005, step=0.001)
b_PTFE = st.sidebar.number_input("PTFE thickness b_PTFE [m]", value=0.005, step=0.001)

# -----------------------------
# ΔT function
# -----------------------------
def calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE):
    return 0.11 * (mu * Fn) * v**0.71 * r**0.30 * r_d**(-1.70) * b**(-0.23) * b_PTFE**0.36

# -----------------------------
# Compute ΔT map
# -----------------------------
v_values = np.linspace(v_min, v_max, 50)
r_values = np.linspace(r_min, r_max, 50)

delta_T_map = np.zeros((len(r_values), len(v_values)))
for i, r_i in enumerate(r_values):
    for j, v_j in enumerate(v_values):
        delta_T_map[i, j] = calc_delta_Tc(mu, Fn, v_j, r_i, r_d, b, b_PTFE)

# Convert to DataFrame for Plotly
df = pd.DataFrame(delta_T_map, index=r_values, columns=v_values)
df.index.name = "Sliding radius r [m]"
df.columns.name = "Sliding velocity v [m/s]"

# -----------------------------
# Plotly heatmap
# -----------------------------
st.subheader("ΔT Heatmap (Sliding radius vs Velocity)")
fig = px.imshow(
    df.values,
    x=df.columns,
    y=df.index,
    color_continuous_scale="hot",
    origin='lower',
    labels=dict(x="Sliding velocity v [m/s]", y="Sliding radius r [m]", color="ΔT [°C]"),
    aspect="auto",
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Download CSV
# -----------------------------
st.subheader("Download Full ΔT Map")
csv = df.to_csv().encode('utf-8')
st.download_button("💾 Download CSV", csv, "deltaT_map.csv", "text/csv")
"text/csv")
























