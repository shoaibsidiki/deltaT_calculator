import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="ΔTc Calculator",
    layout="wide"
)

st.title("ΔTc Calculator")
st.markdown("This app calculates the contact temperature rise (ΔT) based on your input parameters.")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("Input Parameters (SI units)")

# No limits for friction and normal force
mu = st.sidebar.number_input("Friction coefficient μ [-]", value=0.1, step=0.01, format="%.3f")
Fn = st.sidebar.number_input("Normal force Fₙ [N]", value=100.0, step=1.0, format="%.2f")

# Sliders with limits converted to meters
v = st.sidebar.slider("Sliding velocity v [m/s]", 0.25, 1.0, 0.25, 0.01)
r = st.sidebar.slider("Sliding radius r [m]", 0.009, 0.019, 0.009, 0.001)
r_d = st.sidebar.slider("Steel disc radius r_d [m]", 0.025, 0.060, 0.025, 0.001)
b = st.sidebar.slider("Steel disc thickness b [m]", 0.005, 0.015, 0.005, 0.001)
b_PTFE = st.sidebar.slider("PTFE thickness b_PTFE [m]", 0.005, 0.015, 0.005, 0.001)

st.sidebar.markdown("---")
st.sidebar.markdown("Contact temperature calculator for poly-steel")

# -----------------------------
# ΔT calculation function
# -----------------------------
def calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE):
    return 0.11 * (mu * Fn) * v**0.71 * r**0.30 * r_d**(-1.70) * b**(-0.23) * b_PTFE**0.36

# -----------------------------
# Main calculation
# -----------------------------
if st.sidebar.button("Calculate ΔTc"):
    if 0 in [Fn, v, r, r_d, b, b_PTFE]:
        st.error("All input values must be greater than zero.")
    else:
        delta_Tc = calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE)
        st.success(f"### ΔTc = {delta_Tc:.2f} °C")

        # -----------------------------
        # Tabs for outputs
        # -----------------------------
        tabs = st.tabs(["ΔT vs Velocity", "ΔT vs Normal Force", "Heatmap", "Download CSV"])

        # ΔT vs Velocity
        with tabs[0]:
            v_range = np.linspace(v*0.25, v*1.0, 50)
            delta_v = [calc_delta_Tc(mu, Fn, vi, r, r_d, b, b_PTFE) for vi in v_range]
            df_v = pd.DataFrame({"Velocity [m/s]": v_range, "ΔT [°C]": delta_v}).set_index("Velocity [m/s]")
            st.line_chart(df_v)

        # ΔT vs Normal Force
        with tabs[1]:
            Fn_range = np.linspace(Fn*0.1, Fn*5, 50)
            delta_fn = [calc_delta_Tc(mu, Fni, v, r, r_d, b, b_PTFE) for Fni in Fn_range]
            df_fn = pd.DataFrame({"Normal Force [N]": Fn_range, "ΔT [°C]": delta_fn}).set_index("Normal Force [N]")
            st.line_chart(df_fn)

        # Heatmap: ΔT vs Fn and v
        with tabs[2]:
            v_grid = np.linspace(v*0.25, v*1.0, 25)
            Fn_grid = np.linspace(Fn*0.1, Fn*5, 25)
            heatmap = np.zeros((len(Fn_grid), len(v_grid)))
            for i, Fni in enumerate(Fn_grid):
                for j, vj in enumerate(v_grid):
                    heatmap[i, j] = calc_delta_Tc(mu, Fni, vj, r, r_d, b, b_PTFE)
            df_heatmap = pd.DataFrame(
                heatmap,
                index=[f"{f:.1f}" for f in Fn_grid],
                columns=[f"{v_:.2f}" for v_ in v_grid]
            )
            st.dataframe(df_heatmap.style.background_gradient(cmap="YlOrRd"))

        # Download CSV
        with tabs[3]:
            df_csv = pd.DataFrame({
                "μ": [mu],
                "Fₙ [N]": [Fn],
                "v [m/s]": [v],
                "r [m]": [r],
                "r_d [m]": [r_d],
                "b [m]": [b],
                "b_PTFE [m]": [b_PTFE],
                "ΔT [°C]": [delta_Tc]
            })
            csv = df_csv.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "deltaT_results.csv", "text/csv")

st.markdown(
    """
---
**Mobile tip:** Open this page in your phone browser → Add to Home Screen → works like a real app.
"""
)


















