import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Beam Analysis Calculator", layout="wide")

st.title("Beam Analysis Calculator")

# Layout: Use two columns to organize inputs
col1, col2 = st.columns(2)

with col1:
    beam_length = st.slider("Beam Length (meters)", 1.0, 100.0, 10.0)
    num_point_loads = st.slider("Number of Point Loads", 0, 5, 1)
    with st.expander("Point Loads Details"):
        point_loads = []
        for i in range(num_point_loads):
            mag = st.number_input(f"Point Load {i+1} Magnitude (kN)", value=5.0, key=f"pl_mag_{i}")
            pos = st.slider(f"Point Load {i+1} Position (m)", 0.0, beam_length, 2.0, key=f"pl_pos_{i}")
            point_loads.append((mag, pos))

with col2:
    num_udls = st.slider("Number of UDLs", 0, 3, 1)
    with st.expander("UDLs Details"):
        udls = []
        for i in range(num_udls):
            mag = st.number_input(f"UDL {i+1} Magnitude (kN/m)", value=2.0, key=f"udl_mag_{i}")
            start = st.slider(f"UDL {i+1} Start Position (m)", 0.0, beam_length, 4.0, key=f"udl_start_{i}")
            end = st.slider(f"UDL {i+1} End Position (m)", start, beam_length, 8.0, key=f"udl_end_{i}")
            udls.append((mag, start, end))

# Calculations remain the same
moment_sum = 0.0
vertical_load_sum = 0.0
for load, pos in point_loads:
    vertical_load_sum += load
    moment_sum += load * pos
for magnitude, start, end in udls:
    length_udl = end - start
    load_total = magnitude * length_udl
    vertical_load_sum += load_total
    moment_sum += load_total * (start + length_udl / 2)

Rb = moment_sum / beam_length
Ra = vertical_load_sum - Rb

st.markdown(f"**Reaction at Left Support (Ra):** {Ra:.2f} kN")
st.markdown(f"**Reaction at Right Support (Rb):** {Rb:.2f} kN")

# Discretize beam
x = np.linspace(0, beam_length, 500)
shear = np.zeros_like(x)
moment = np.zeros_like(x)

for i, xi in enumerate(x):
    V = Ra
    M = Ra * xi
    for load, pos in point_loads:
        if xi >= pos:
            V -= load
            M -= load * (xi - pos)
    for magnitude, start, end in udls:
        if xi >= start:
            length_seg = min(xi, end) - start
            if length_seg > 0:
                load_seg = magnitude * length_seg
                V -= load_seg
                M -= load_seg * (xi - (start + length_seg / 2))
    shear[i] = V
    moment[i] = M

# Use Plotly for interactive plotting
fig = go.Figure()

fig.add_trace(go.Scatter(x=x, y=shear, mode='lines', name='Shear Force (kN)', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=x, y=moment, mode='lines', name='Bending Moment (kNm)', line=dict(color='red')))

fig.update_layout(
    title="Shear Force and Bending Moment Diagrams",
    xaxis_title="Distance along beam (m)",
    yaxis_title="Force / Moment",
    legend_title="Legend",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)
