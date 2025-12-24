import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="🔥 ΔTc Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 style='text-align: center; color: darkblue;'>🔥 ΔTc Calculator</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Calculate contact temperature rise based on friction, force, velocity and geometry.</p>", 
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Inputs with expanders
# -----------------------------
with st.sidebar.expander("Input Parameters (SI units)", expanded=True):
    mu = st.number_input("Friction coefficient μ [-]", value=0.1, step=0.01, format="%.3f",
                         help="Coefficient of friction (no limit)")
    Fn = st.number_input("Normal force Fₙ [N]", value=100.0, step=1.0, format="%.2f",
                         help="Force applied on the interface (no limit)")
    v = st.number_input("Sliding velocity v [m/s]", 0.25, 1.0, 0.25, 0.01)
    r = st.number_input("Sliding radius r [m]", 0.009, 0.019, 0.009, 0.001)
    r_d = st.number_input("Steel disc radius r_d [m]", 0.025, 0.060, 0.025, 0.001)
    b = st.number_input("Steel disc thickness b [m]", 0.005, 0.015, 0.005, 0.001)
    b_PTFE = st.number_input("PTFE thickness b_PTFE [m]", 0.005, 0.015, 0.005, 0.001)

st.sidebar.markdown("---")
st.sidebar.markdown("Polymer-steel contact temperature calculator 🚀")

# -----------------------------
# ΔT calculation function
# -----------------------------
def calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE):
    return 0.11 * (mu * Fn) * v**0.71 * r**0.30 * r_d**(-1.70) * b**(-0.23) * b_PTFE**0.36

# -----------------------------
# Calculate ΔT
# -----------------------------
delta_Tc = calc_delta_Tc(mu, Fn, v, r, r_d, b, b_PTFE)

# -----------------------------
# Show metrics on top
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric(label="ΔT₍c₎ [°C] 🔥", value=f"{delta_Tc:.2f}")
col2.metric(label="Sliding velocity [m/s] ⚡", value=f"{v}")
col3.metric(label="Normal force [N] 🏋️", value=f"{Fn}")

# -----------------------------
# Tabs for outputs
# -----------------------------
tabs = st.tabs(["📈 ΔT vs Velocity", "📊 ΔT vs Force", "🌡 Heatmap", "💾 Download CSV"])

with tabs[0]:
    st.subheader("ΔT vs Sliding Velocity")
    v_range = np.linspace(0.25, 1.0, 50)
    delta_v = [calc_delta_Tc(mu, Fn, vi, r, r_d, b, b_PTFE) for vi in v_range]
    df_v = pd.DataFrame({"Velocity [m/s]": v_range, "ΔT [°C]": delta_v}).set_index("Velocity [m/s]")
    st.line_chart(df_v, use_container_width=True)

with tabs[1]:
    st.subheader("ΔT vs Normal Force")
    Fn_range = np.linspace(Fn*0.1, Fn*5, 50)
    delta_fn = [calc_delta_Tc(mu, Fni, v, r, r_d, b, b_PTFE) for Fni in Fn_range]
    df_fn = pd.DataFrame({"Normal Force [N]": Fn_range, "ΔT [°C]": delta_fn}).set_index("Normal Force [N]")
    st.line_chart(df_fn, use_container_width=True)

with tabs[2]:
    st.subheader("Heatmap: ΔT vs Fn & Velocity")
    v_grid = np.linspace(0.25, 1.0, 25)
    Fn_grid = np.linspace(Fn*0.1, Fn*5, 25)
    heatmap = np.zeros((len(Fn_grid), len(v_grid)))
    for i, Fni in enumerate(Fn_grid):
        for j, vj in enumerate(v_grid):
            heatmap[i, j] = calc_delta_Tc(mu, Fni, vj, r, r_d, b, b_PTFE)
    df_heatmap = pd.DataFrame(heatmap, index=[f"{f:.1f}" for f in Fn_grid],
                              columns=[f"{v_:.2f}" for v_ in v_grid])
    st.dataframe(df_heatmap.style.background_gradient(cmap="coolwarm"))

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
    st.download_button("💾 Download CSV", csv, "deltaT_results.csv", "text/csv")

st.markdown(
    """
---
**Mobile tip:** Open this page in your phone browser → Add to Home Screen → works like a real app 🚀
"""
)




























