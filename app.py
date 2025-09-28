import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="DER Integration Analytics",
    page_icon="⚡",
    layout="wide"
)

# Modern gradient CSS for Bolt.new
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.4);
    }
    
    .ev-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .solar-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
    }
    
    .capacity-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Generate sample data
@st.cache_data
def generate_der_data():
    np.random.seed(42)
    
    # EV Chargers
    ev_data = []
    for i in range(500):
        ev_data.append({
            'charger_id': f'EV_{i:03d}',
            'power_kw': np.random.uniform(7, 150),
            'location': np.random.choice(['Residential', 'Commercial', 'Public']),
            'utilization': np.random.uniform(0.2, 0.9)
        })
    
    # Solar Systems
    solar_data = []
    for i in range(1000):
        solar_data.append({
            'system_id': f'PV_{i:03d}',
            'capacity_kw': np.random.choice([5, 10, 15, 20, 50]),
            'generation_kwh': np.random.uniform(20, 200),
            'type': np.random.choice(['Residential', 'Commercial', 'Utility'])
        })
    
    # Feeders
    feeder_data = []
    for i in range(50):
        feeder_data.append({
            'feeder_id': f'FEEDER_{i:02d}',
            'capacity_mva': np.random.choice([5, 10, 15, 20]),
            'load_pct': np.random.uniform(60, 95),
            'ev_penetration': np.random.uniform(5, 20),
            'solar_penetration': np.random.uniform(10, 40)
        })
    
    return pd.DataFrame(ev_data), pd.DataFrame(solar_data), pd.DataFrame(feeder_data)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ DER Integration Analytics</h1>
        <p>Grid Decarbonization Enablement Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    ev_df, solar_df, feeder_df = generate_der_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card ev-card">
            <h3>EV Chargers</h3>
            <h2>500</h2>
            <p>Active stations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card solar-card">
            <h3>Solar Systems</h3>
            <h2>1,000</h2>
            <p>Connected inverters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card capacity-card">
            <h3>Total Capacity</h3>
            <h2>750 MVA</h2>
            <p>Distribution system</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Feeders</h3>
            <h2>50</h2>
            <p>Monitored circuits</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 DER Overview", "⚡ Load Analysis", "🔧 Planning"])
    
    with tab1:
        st.subheader("DER Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # EV charger distribution
            fig_ev = px.pie(
                ev_df, 
                names='location', 
                title="EV Charger Distribution by Location",
                color_discrete_sequence=['#667eea', '#4facfe', '#f093fb']
            )
            st.plotly_chart(fig_ev, use_container_width=True)
        
        with col2:
            # Solar capacity by type
            solar_summary = solar_df.groupby('type')['capacity_kw'].sum().reset_index()
            fig_solar = px.bar(
                solar_summary,
                x='type',
                y='capacity_kw',
                title="Solar Capacity by Installation Type",
                color='capacity_kw',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig_solar, use_container_width=True)
    
    with tab2:
        st.subheader("Load Impact Analysis")
        
        # Feeder loading analysis
        fig_load = px.scatter(
            feeder_df,
            x='capacity_mva',
            y='load_pct',
            size='ev_penetration',
            color='solar_penetration',
            title="Feeder Capacity vs Loading",
            labels={'load_pct': 'Load (%)', 'capacity_mva': 'Capacity (MVA)'}
        )
        fig_load.add_hline(y=85, line_dash="dash", line_color="red", annotation_text="Constraint Threshold")
        st.plotly_chart(fig_load, use_container_width=True)
        
        # DER penetration
        col1, col2 = st.columns(2)
        
        with col1:
            avg_ev = feeder_df['ev_penetration'].mean()
            st.metric("Average EV Penetration", f"{avg_ev:.1f}%")
        
        with col2:
            avg_solar = feeder_df['solar_penetration'].mean()
            st.metric("Average Solar Penetration", f"{avg_solar:.1f}%")
    
    with tab3:
        st.subheader("Infrastructure Planning")
        
        # High-load feeders
        high_load = feeder_df[feeder_df['load_pct'] > 85]
        
        if len(high_load) > 0:
            st.warning(f"⚠️ {len(high_load)} feeders above 85% loading threshold")
            st.dataframe(high_load[['feeder_id', 'capacity_mva', 'load_pct']], use_container_width=True)
        else:
            st.success("✅ All feeders within capacity limits")
        
        # Investment summary
        st.subheader("Investment Requirements")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Upgrades Needed", len(high_load))
        
        with col2:
            investment = len(high_load) * 2.5  # $2.5M per upgrade
            st.metric("Total Investment", f"${investment:.1f}M")
        
        with col3:
            capacity_added = len(high_load) * 5  # 5 MVA per upgrade
            st.metric("Capacity Added", f"{capacity_added} MVA")

if __name__ == "__main__":
    main()
