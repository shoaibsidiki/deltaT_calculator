import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="ΔTc Calculator",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("ΔT(C) Calculator")
st.markdown("**All inputs must be in SI units**")

st.divider()

# -----------------------------
# Inputs
# -----------------------------
st.subheader("Input Parameters")

mu = st.number_input(
    label="Friction coefficient μ [-]",
    min_value=0.0,
    value=0.1,
    step=0.01,
    format="%.3f",
    key="mu"
)
Fn = st.number_input(
    label="Normal force Fₙ [N]",
    min_value=0.0,
    value=100.0,
    step=1.0,
    format="%.2f",
    key="Fn"
)
v = st.number_input(
    label="Sliding velocity v [m/s]",
    min_value=0.0,
    value=0.1,
    step=0.01,
    format="%.3f",
    key="v"
)

r = st.number_input(
    label="Sliding radius r [m]",
    min_value=0.001,
    max_value=0.1,
    value=0.01,
    step=0.001,
    format="%.4f",
    key="r"
)
r_d = st.number_input(
    label="Steel disc radius r_d [m]",
    min_value=0.001,
    max_value=0.1,
    value=0.01,
    step=0.001,
    format="%.4f",
    key="r_d"
)
b = st.number_input(
    label="Steel disc thickness b [m]",
    min_value=0.001,
    max_value=0.05,
    value=0.005,
    step=0.001,
    format="%.4f",
    key="b"
)
b_PTFE = st.number_input(
    label="PTFE thickness b_PTFE [m]",
    min_value=0.0005,
    max_value=0.01,
    value=0.001,
    step=0.0005,
    format="%.4f",
    key="b_PTFE"
)

st.divider()

# -----------------------------
# Calculation function
# -----------------------------
def calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE):
    return 0.11 * (mu * Fn) * v**0.71 * r**0.30 * r_d**(-1.70) * b**(-0.23) * b_PTFE**0.36

# -----------------------------
# Compute main ΔT
# -----------------------------
if st.button("Calculate ΔTc", key="calculate_button"):
    # Validate inputs
    if 0 in [Fn, v, r, r_d, b, b_PTFE]:
        st.error("All input values must be greater than zero.")
    else:
        delta_Tc = calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE)
        st.success(f"ΔT₍c₎ = {delta_Tc:.2f} °C")

        # -----------------------------
        # Sensitivity vs velocity
        # -----------------------------
        v_range = np.linspace(v*0.1, v*5, 50)
        delta_v = [calc_delta_Tc(mu, Fn, vi, r, r_d, b, b_PTFE) for vi in v_range]
        df_v = pd.DataFrame({"Velocity [m/s]": v_range, "ΔT₍c₎ [°C]": delta_v}).set_index("Velocity [m/s]")
        st.subheader("ΔT vs Sliding Velocity")
        st.line_chart(df_v)

        # -----------------------------
        # Sensitivity vs normal force
        # -----------------------------
        Fn_range = np.linspace(Fn*0.1, Fn*5, 50)
        delta_fn = [calc_delta_Tc(mu, Fni, v, r, r_d, b, b_PTFE) for Fni in Fn_range]
        df_fn = pd.DataFrame({"Normal Force [N]": Fn_range, "ΔT₍c₎ [°C]": delta_fn}).set_index("Normal Force [N]")
        st.subheader("ΔT vs Normal Force")
        st.line_chart(df_fn)

        # -----------------------------
        # Heatmap: ΔT vs Fn and v
        # -----------------------------
        v_grid = np.linspace(v*0.5, v*2, 25)
        Fn_grid = np.linspace(Fn*0.5, Fn*2, 25)
        heatmap = np.zeros((len(Fn_grid), len(v_grid)))

        for i, Fni in enumerate(Fn_grid):
            for j, vj in enumerate(v_grid):
                heatmap[i, j] = calc_delta_Tc(mu, Fni, vj, r, r_d, b, b_PTFE)

        df_heatmap = pd.DataFrame(
            heatmap,
            index=[f"{f:.1f}" for f in Fn_grid],
            columns=[f"{v_:.2f}" for v_ in v_grid]
        )
        st.subheader("ΔT Heatmap (Fn vs v)")
        st.dataframe(df_heatmap.style.background_gradient(cmap="YlOrRd"))

        # -----------------------------
        # CSV export
        # -----------------------------
        df_csv = pd.DataFrame({
            "μ": [mu],
            "Fₙ [N]": [Fn],
            "v [m/s]": [v],
            "r [m]": [r],
            "r_d [m]": [r_d],
            "b [m]": [b],
            "b_PTFE [m]": [b_PTFE],
            "ΔT₍c₎ [°C]": [delta_Tc]
        })
        csv = df_csv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Result as CSV",
            data=csv,
            file_name='delta_Tc_results.csv',
            mime='text/csv',
            key="download_csv"
        )

st.markdown(
    """
---
**Mobile tip:** Open this page in your phone browser → Add to Home Screen → works like a real app.
"""
)










