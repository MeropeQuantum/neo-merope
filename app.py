import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from utils.quantum_simulator import QuantumSimulator
from utils.data_generator import DataGenerator
from utils.db_integration import db_manager
from utils.styling import (
    apply_enterprise_style, create_enterprise_metric_card, 
    create_status_badge, get_enterprise_plotly_theme,
    create_enterprise_header, create_alert_box, EnterpriseTheme
)
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Merope - Quantum Control Platform",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply enterprise styling
apply_enterprise_style()

# Initialize session state
if 'quantum_sim' not in st.session_state:
    st.session_state.quantum_sim = QuantumSimulator()
if 'data_gen' not in st.session_state:
    st.session_state.data_gen = DataGenerator()
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()

# Enhanced sidebar with professional dark theme
st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border: 1px solid #333333;">
    <h2 style="color: #ffffff; margin: 0; font-size: 1.8rem; font-weight: 700; text-shadow: 0 0 10px rgba(255,255,255,0.3);">🔮 MEROPE</h2>
    <p style="color: #888888; margin: 0.5rem 0 0 0; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 1px;">Quantum Control Platform</p>
</div>
""", unsafe_allow_html=True)

# System status overview in sidebar
st.sidebar.markdown("### 📊 System Status")
system_health_data = {
    "Active Qubits": ("8/8", "operational"),
    "Cryogenic Temp": ("15 mK", "operational"), 
    "System Uptime": ("99.7%", "operational"),
    "Avg Coherence": ("125 μs", "operational")
}

for metric, (value, status) in system_health_data.items():
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid #ffffff; border: 1px solid #333333;">
        <div style="font-size: 0.75rem; color: #888888; margin-bottom: 0.25rem; text-transform: uppercase; letter-spacing: 1px;">{metric}</div>
        <div style="font-size: 1.125rem; font-weight: 600; color: #ffffff; text-shadow: 0 0 8px rgba(255,255,255,0.3);">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

# Enhanced auto-refresh controls
st.sidebar.markdown("### ⚙️ Controls")
auto_refresh = st.sidebar.checkbox("🔄 Real-time Updates", value=True)
refresh_rate = 2  # Default value
if auto_refresh:
    refresh_rate = st.sidebar.selectbox("Update Interval", [1, 2, 5, 10], index=1, format_func=lambda x: f"{x}s")
    st.sidebar.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); padding: 0.5rem; border-radius: 6px; margin-top: 0.5rem; border: 1px solid #333333;">
        <small style="color: #888888; text-transform: uppercase; letter-spacing: 1px;">Last update: {st.session_state.last_update.strftime('%H:%M:%S')}</small>
    </div>
    """, unsafe_allow_html=True)

# Main header with professional dark theme
st.markdown(create_enterprise_header(
    "MEROPE Control Center",
    "Professional quantum computing control and monitoring platform",
    "operational"
), unsafe_allow_html=True)

# Enterprise key metrics dashboard
col1, col2, col3, col4 = st.columns(4)

metrics_data = [
    ("Average Gate Fidelity", "98.7%", "+0.3%", "normal"),
    ("Error Rate", "0.13%", "-0.02%", "inverse"),
    ("Readout Fidelity", "99.2%", "+0.1%", "normal"),
    ("Crosstalk Level", "2.1%", "-0.4%", "inverse")
]

for i, (col, (title, value, delta, delta_color)) in enumerate(zip([col1, col2, col3, col4], metrics_data)):
    with col:
        st.markdown(create_enterprise_metric_card(title, value, delta, delta_color), unsafe_allow_html=True)

st.markdown("---")

# Recent activity and alerts
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📊 Live Telemetry Overview")
    
    # Generate sample telemetry data
    current_time = datetime.now()
    time_points = [current_time - timedelta(seconds=i) for i in range(30, 0, -1)]
    
    # Create multi-qubit telemetry plot with enterprise styling
    fig = go.Figure()
    
    # Generate telemetry data from database or simulate
    try:
        dashboard_data = db_manager.get_dashboard_data(hours=1)
        telemetry_df = dashboard_data.get('telemetry', pd.DataFrame())
        
        if not telemetry_df.empty:
            # Use real data from database
            for qubit_id in range(min(4, telemetry_df['qubit_id'].nunique())):
                qubit_data = telemetry_df[telemetry_df['qubit_id'] == qubit_id]
                if not qubit_data.empty:
                    qubit_data = qubit_data.sort_values('timestamp')
                    fig.add_trace(go.Scatter(
                        x=pd.to_datetime(qubit_data['timestamp']),
                        y=qubit_data['frequency_ghz'],
                        mode='lines+markers',
                        name=f'Qubit {qubit_id}',
                        line=dict(width=3, color=EnterpriseTheme.CHART_COLORS[qubit_id]),
                        marker=dict(size=6)
                    ))
        else:
            # Generate sample data if no database data
            telemetry_data = st.session_state.data_gen.generate_qubit_telemetry(num_points=30, hours=1)
            for qubit_id in range(4):
                qubit_data = telemetry_data[telemetry_data['qubit_id'] == qubit_id]
                if not qubit_data.empty:
                    fig.add_trace(go.Scatter(
                        x=pd.to_datetime(qubit_data['timestamp']),
                        y=qubit_data['frequency_ghz'],
                        mode='lines+markers',
                        name=f'Qubit {qubit_id}',
                        line=dict(width=3, color=EnterpriseTheme.CHART_COLORS[qubit_id]),
                        marker=dict(size=6)
                    ))
    except Exception as e:
        st.error(f"Error loading frequency data: {str(e)}")
        # Fallback to basic visualization
        for qubit_id in range(4):
            base_freq = 4.5 + qubit_id * 0.2
            frequencies = [base_freq + np.random.normal(0, 0.001) for _ in range(30)]
            fig.add_trace(go.Scatter(
                x=time_points,
                y=frequencies,
                mode='lines+markers',
                name=f'Qubit {qubit_id}',
                line=dict(width=3, color=EnterpriseTheme.CHART_COLORS[qubit_id]),
                marker=dict(size=6)
            ))
    
    # Apply enterprise theme
    enterprise_theme = get_enterprise_plotly_theme()
    fig.update_layout(
        title={
            'text': "Qubit Transition Frequencies",
            'font': {'size': 18, 'color': '#ffffff'}
        },
        xaxis_title="Time",
        yaxis_title="Frequency (GHz)",
        height=450,
        showlegend=True,
        **enterprise_theme['layout']
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🚨 System Alerts")
    
    # Enhanced alert system with enterprise styling
    alerts = [
        {"level": "info", "message": "Calibration scheduled in 2h", "time": "10:30", "priority": "low"},
        {"level": "warning", "message": "Q3 coherence below threshold", "time": "10:15", "priority": "medium"},
        {"level": "success", "message": "Auto-tune completed", "time": "10:00", "priority": "low"},
        {"level": "info", "message": "Daily backup completed", "time": "09:45", "priority": "low"}
    ]
    
    for alert in alerts:
        alert_message = f"[{alert['time']}] {alert['message']}"
        st.markdown(create_alert_box(alert_message, alert["level"]), unsafe_allow_html=True)

# Enterprise system architecture overview
st.markdown("### 🏗️ System Architecture")

col1, col2, col3 = st.columns(3)

architecture_components = [
    ("Control Layer", ["Pulse Generation", "Real-time Feedback", "Error Correction", "Calibration Control"], "#ffffff"),
    ("Hardware Layer", ["Dilution Refrigerator", "Microwave Electronics", "Readout Systems", "RF Components"], "#00ff88"),
    ("Software Layer", ["Quantum Compiler", "Calibration Engine", "Data Pipeline", "Analytics Engine"], "#ffaa00")
]

for col, (layer_name, components, color) in zip([col1, col2, col3], architecture_components):
    with col:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); 
                    padding: 1.5rem; border-radius: 12px; border-left: 4px solid {color}; height: 220px; border: 1px solid #333333;">
            <h4 style="color: {color}; margin-bottom: 1rem; font-weight: 600; text-shadow: 0 0 8px rgba({color[1:]}, 0.5); text-transform: uppercase; letter-spacing: 1px;">{layer_name}</h4>
            {"".join([f'<div style="color: #cccccc; margin-bottom: 0.5rem; padding: 0.25rem 0;">• {comp}</div>' for comp in components])}
        </div>
        """, unsafe_allow_html=True)

# Enhanced navigation with professional black styling
st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); 
            padding: 1.5rem; border-radius: 12px; border: 1px solid #333333; text-align: center;">
    <h4 style="color: #ffffff; margin-bottom: 0.5rem; text-shadow: 0 0 10px rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 2px;">🔮 NAVIGATION</h4>
    <p style="color: #888888; margin: 0; text-transform: uppercase; letter-spacing: 1px;">Use the sidebar to access detailed monitoring and control interfaces</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh mechanism
if auto_refresh:
    time.sleep(refresh_rate)
    st.session_state.last_update = datetime.now()
    st.rerun()
