import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(
    page_title="WiseClaw OS",
    layout="wide",
    page_icon="🦁",
    initial_sidebar_state="expanded"
)

STATE_FILE = "data/system_state.json"
CSS_FILE = "src/dashboard/style.css"

# --- LOADERS ---
def load_css():
    with open(CSS_FILE, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except: return {}

# --- VIEWS ---
def view_overview(state):
    st.markdown("## 🚀 Mission Control")
    
    # Top KPIs
    agents = state.get("agents", {})
    active = sum(1 for a in agents.values() if a.get("status") == "Busy")
    total = len(agents)
    usage = state.get("global_token_usage", 0)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Agents", f"{active}/{total}", delta="Operational")
    c2.metric("Token Burn", f"{usage/1000:.1f}k", delta="Normal", delta_color="normal")
    c3.metric("System Health", state.get("system_health", "Unknown"), delta="Stable")
    c4.metric("Sprint Phase", state.get("sprint", "N/A"))

    st.markdown("---")
    
    # Main Content Split
    col_grid, col_charts = st.columns([3, 2])
    
    with col_grid:
        st.subheader("🧩 Neural Grid")
        agent_list = list(agents.items())
        for i in range(0, len(agent_list), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(agent_list):
                    name, data = agent_list[i+j]
                    status = data.get("status", "Idle")
                    status_cls = status.lower()
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div class="agent-card {status_cls}">
                            <div class="agent-header">
                                <span class="agent-name">{name}</span>
                                <span class="agent-status-badge status-{status_cls}">{status}</span>
                            </div>
                            <div class="agent-role">{data.get('model')}</div>
                            <div class="agent-task">{data.get('current_task', 'Awaiting directives...')}</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col_charts:
        st.subheader("📈 Live Telemetry")
        
        # Mock Timeline Data (Simulating Gantt)
        df_timeline = pd.DataFrame([
            dict(Task="Research", Start='2026-02-14 10:00', Finish='2026-02-14 10:30', Resource="Researcher"),
            dict(Task="Dev API", Start='2026-02-14 10:15', Finish='2026-02-14 11:00', Resource="Coder"),
            dict(Task="Audit", Start='2026-02-14 11:00', Finish='2026-02-14 11:15', Resource="Critic")
        ])
        fig_timeline = px.timeline(df_timeline, x_start="Start", x_end="Finish", y="Resource", color="Resource", template="plotly_dark")
        fig_timeline.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_timeline, use_container_width=True)

        # Token Usage Area Chart (Mock)
        st.caption("Token Consumption (Last 1h)")
        chart_data = pd.DataFrame(
            [[10, 20, 30], [20, 30, 50], [30, 40, 60]],
            columns=['Manager', 'Coder', 'Researcher']
        )
        st.area_chart(chart_data, height=200)

def view_logs():
    st.markdown("## 📜 System Logs")
    st.code("2026-02-14 23:55:01 [INFO] Manager: Initializing Sprint 3...\n2026-02-14 23:55:05 [INFO] Researcher: Querying Google Gemini...\n2026-02-14 23:55:10 [WARN] Coder: Deprecated library detected...", language="log")

# --- MAIN ---
load_css()
state = load_state()

# Sidebar
with st.sidebar:
    st.title("🦁 WiseClaw")
    page = st.radio("Navigation", ["Mission Control", "Task Timeline", "System Logs", "Settings"])
    st.divider()
    st.info(f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
    if st.button("🔄 Refresh Data"):
        st.rerun()

if page == "Mission Control":
    view_overview(state)
elif page == "System Logs":
    view_logs()
else:
    st.warning("Module under construction.")
