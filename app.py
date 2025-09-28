import streamlit as st
import pandas as pd
import numpy as np

# Only import plotly if available
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available - using basic charts")

from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="DER Integration Analytics",
    page_icon="⚡",
    layout="wide"
)

# Simplified CSS that works in all environments
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        border: 2px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Generate simple sample data
@st.cache_data
def get_sample_data():
    """Generate basic sample data for demonstration"""
    np.random.seed(42)
    
    # EV Chargers data
    ev_data = {
        'location': ['Residential'] * 350 + ['Commercial'] * 100 + ['Public'] * 50,
        'power_kw': np.random.uniform(7, 150, 500),
        'utilization': np.random.uniform(0.2, 0.9, 500)
    }
    
    # Solar data
    solar_data = {
        'type': ['Residential'] * 700 + ['Commercial'] * 250 + ['Utility'] * 50,
        'capacity_kw': np.random.choice([5, 10, 15, 20, 50], 1000),
        'generation': np.random.uniform(20, 200, 1000)
    }
    
    # Feeder data
    feeder_data = {
        'feeder_id': [f'FEEDER_{i:02d}' for i in range(50)],
        'capacity_mva': np.random.choice([5, 10, 15, 20], 50),
        'load_pct': np.random.uniform(60, 95, 50),
        'ev_penetration': np.random.uniform(5, 20, 50),
        'solar_penetration': np.random.uniform(10, 40, 50)
    }
    
    return (pd.DataFrame(ev_data), 
            pd.DataFrame(solar_data), 
            pd.DataFrame(feeder_data))

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ DER Integration Analytics</h1>
        <p>Grid Decarbonization Enablement Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Load data
        ev_df, solar_df, feeder_df = get_sample_data()
        
        st.success("✅ Application loaded successfully!")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>EV Chargers</h4>
                <div class="metric-value">500</div>
                <p>Active stations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>Solar Systems</h4>
                <div class="metric-value">1,000</div>
                <p>Connected inverters</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>Total Capacity</h4>
                <div class="metric-value">750 MVA</div>
                <p>Distribution system</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h4>Feeders</h4>
                <div class="metric-value">50</div>
                <p>Monitored circuits</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚡ Analysis", "🔧 Planning"])
        
        with tab1:
            st.subheader("DER Distribution Overview")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**EV Charger Distribution by Location:**")
                location_counts = ev_df['location'].value_counts()
                st.dataframe(location_counts)
                
                if PLOTLY_AVAILABLE:
                    fig = px.pie(values=location_counts.values, names=location_counts.index, 
                               title="EV Charger Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.bar_chart(location_counts)
            
            with col2:
                st.write("**Solar Installation Types:**")
                solar_counts = solar_df['type'].value_counts()
                st.dataframe(solar_counts)
                
                if PLOTLY_AVAILABLE:
                    fig = px.bar(x=solar_counts.index, y=solar_counts.values,
                               title="Solar Installations by Type")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.bar_chart(solar_counts)
        
        with tab2:
            st.subheader("Load Analysis")
            
            # Feeder analysis
            st.write("**Feeder Loading Analysis:**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                avg_load = feeder_df['load_pct'].mean()
                st.metric("Average Feeder Loading", f"{avg_load:.1f}%")
                
                high_load = feeder_df[feeder_df['load_pct'] > 85]
                st.metric("High Load Feeders (>85%)", len(high_load))
            
            with col2:
                avg_ev = feeder_df['ev_penetration'].mean()
                st.metric("Average EV Penetration", f"{avg_ev:.1f}%")
                
                avg_solar = feeder_df['solar_penetration'].mean()
                st.metric("Average Solar Penetration", f"{avg_solar:.1f}%")
            
            # Show feeder data
            st.write("**Feeder Details:**")
            display_df = feeder_df[['feeder_id', 'capacity_mva', 'load_pct', 'ev_penetration', 'solar_penetration']].round(1)
            st.dataframe(display_df, use_container_width=True)
            
            if PLOTLY_AVAILABLE:
                fig = px.scatter(feeder_df, x='capacity_mva', y='load_pct', 
                               size='ev_penetration', color='solar_penetration',
                               title="Feeder Capacity vs Loading")
                fig.add_hline(y=85, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Infrastructure Planning")
            
            # High load feeders
            high_load_feeders = feeder_df[feeder_df['load_pct'] > 85]
            
            if len(high_load_feeders) > 0:
                st.warning(f"⚠️ {len(high_load_feeders)} feeders above 85% loading threshold")
                
                st.write("**Feeders Requiring Attention:**")
                priority_df = high_load_feeders[['feeder_id', 'capacity_mva', 'load_pct']].round(1)
                st.dataframe(priority_df, use_container_width=True)
                
                # Investment metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Upgrades Needed", len(high_load_feeders))
                
                with col2:
                    investment = len(high_load_feeders) * 2.5
                    st.metric("Investment Required", f"${investment:.1f}M")
                
                with col3:
                    capacity = len(high_load_feeders) * 5
                    st.metric("Capacity Added", f"{capacity} MVA")
            else:
                st.success("✅ All feeders operating within normal capacity limits")
            
            # Summary statistics
            st.write("**System Summary:**")
            summary_data = {
                'Metric': ['Total EV Chargers', 'Total Solar Systems', 'Total Feeders', 'Average Load', 'High Risk Feeders'],
                'Value': [500, 1000, 50, f"{feeder_df['load_pct'].mean():.1f}%", len(high_load_feeders)]
            }
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading application: {str(e)}")
        st.write("Please check the console for detailed error information.")

if __name__ == "__main__":
    main()
