import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ΔTc Full Map", layout="wide")
st.title("🔥 ΔTc Full Temperature Map")

# -----------------------------
# Fixed inputs
# -----------------------------
st.sidebar.header("Fixed Inputs")
mu = st.sidebar.number_input("Friction coefficient μ [-]", value=0.1, step=0.01)
Fn = st.sidebar.number_input("Normal force Fₙ [N]", value=100.0, step=1.0)

# -----------------------------
# Parameter ranges
# -----------------------------
st.sidebar.header("Parameter Ranges for ΔT Map")

v_min, v_max = st.sidebar.slider("Sliding velocity v [m/s]", 0.25, 1.0, (0.25, 1.0), 0.01)
r_min, r_max = st.sidebar.slider("Sliding radius r [m]", 0.009, 0.019, (0.009, 0.019), 0.001)

# Fixed geometry values (you can also add sliders for these)
r_d = st.sidebar.number_input("Steel disc radius r_d [m]", value=0.025, step=0.001)
b = st.sidebar.number_input("Steel disc thickness b [m]", value=0.005, step=0.001)
b_PTFE = st.sidebar.number_input("PTFE thickness b_PTFE [m]", value=0.005, step=0.001)

# -----------------------------
# ΔT function
# -----------------------------
def calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE):
    return 0.11 * (mu * Fn) * v**0.71 * r**0.30 * r_d**(-1.70) * b**(-0.23) * b_PTFE**0.36

# -----------------------------
# Create grid and compute ΔT
# -----------------------------
v_values = np.linspace(v_min, v_max, 50)
r_values = np.linspace(r_min, r_max, 50)
delta_T_map = np.zeros((len(r_values), len(v_values)))

for i, r_i in enumerate(r_values):
    for j, v_j in enumerate(v_values):
        delta_T_map[i, j] = calc_delta_Tc(mu, Fn, v_j, r_i, r_d, b, b_PTFE)

# -----------------------------
# Display heatmap
# -----------------------------
st.subheader("ΔT Heatmap (Sliding radius vs Velocity)")
fig, ax = plt.subplots(figsize=(8, 6))
c = ax.imshow(delta_T_map, origin='lower', aspect='auto',
              extent=[v_min, v_max, r_min, r_max],
              cmap='hot')
ax.set_xlabel("Sliding velocity v [m/s]")
ax.set_ylabel("Sliding radius r [m]")
ax.set_title(f"ΔTc Map at μ={mu}, Fₙ={Fn} N")
fig.colorbar(c, ax=ax, label="ΔT [°C]")
st.pyplot(fig)

# -----------------------------
# Optional: Download CSV
# -----------------------------
st.subheader("Download Full ΔT Map")
df_map = pd.DataFrame(delta_T_map, index=[f"{r:.4f}" for r in r_values],
                      columns=[f"{v:.3f}" for v in v_values])
csv = df_map.to_csv().encode('utf-8')
st.download_button("💾 Download CSV", csv, "deltaT_map.csv", "text/csv")























