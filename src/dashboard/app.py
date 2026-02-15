
import streamlit as st
from src.dashboard.graph_3d import generate_3d_graph

st.set_page_config(page_title="WiseClaw OS v5.0", layout="wide", page_icon="🦅")
st.title("🦅 WiseClaw OS v5.0: Sovereign Intelligence")

tab1, tab2 = st.tabs(["Neural Graph 3D", "System Logs"])

with tab1:
    st.subheader("Neural Knowledge Visualization")
    fig = generate_3d_graph()
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Live System Telemetry")
    # ... lógica de logs existente ...
