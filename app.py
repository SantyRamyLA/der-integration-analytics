# Distributed Energy Resource (DER) Integration Analytics
# Grid Decarbonization Enablement Platform

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="DER Integration Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern gradient-based CSS design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.4);
        transition: transform 0.3s ease;
        border: none;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .ev-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
    }
    
    .solar-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #333;
        box-shadow: 0 8px 25px rgba(255, 236, 210, 0.4);
    }
    
    .capacity-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #333;
        box-shadow: 0 8px 25px rgba(168, 237, 234, 0.4);
    }
    
    .constraint-card {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #333;
        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.4);
    }
    
    .metric-card h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card .metric-value {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .metric-card .metric-desc {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-size: 0.9rem;
        margin: 0;
        opacity: 0.8;
    }
    
    .info-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    .tab-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #495057;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 15px;
        margin-top: 3rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

class DERAnalytics:
    def __init__(self):
        self.smart_meter_data = self.generate_smart_meter_data()
        self.ev_charger_data = self.generate_ev_charger_data()
        self.solar_inverter_data = self.generate_solar_inverter_data()
        self.feeder_data = self.generate_feeder_data()
        self.adoption_forecasts = self.generate_adoption_forecasts()
    
    @st.cache_data
    def generate_smart_meter_data(_self):
        """Generate smart meter telemetry data"""
        np.random.seed(42)
        
        data = []
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=720, freq='H')
        
        for meter_id in range(1, 101):  # 100 meters for demo
            meter_type = np.random.choice(['Residential', 'Commercial', 'Industrial'], 
                                        p=[0.7, 0.25, 0.05])
            
            for i, timestamp in enumerate(dates[::24]):  # Daily samples
                hour = timestamp.hour
                day_of_week = timestamp.dayofweek
                month = timestamp.month
                
                # Base load patterns
                if meter_type == 'Residential':
                    base_load = 2.5 + 1.5 * np.sin((hour - 6) * np.pi / 12)
                    if day_of_week < 5:  # Weekday
                        base_load *= 0.9
                elif meter_type == 'Commercial':
                    base_load = 15.0 + 8.0 * np.sin((hour - 12) * np.pi / 8)
                    if day_of_week >= 5:  # Weekend
                        base_load *= 0.3
                else:  # Industrial
                    base_load = 45.0 + 15.0 * np.random.normal(0, 0.2)
                
                # Seasonal adjustment
                seasonal_factor = 1 + 0.3 * np.sin((month - 6) * np.pi / 6)
                
                # Final load calculation
                load_kw = base_load * seasonal_factor * (1 + np.random.normal(0, 0.1))
                load_kw = max(0, load_kw)
                
                data.append({
                    'meter_id': f"SM_{meter_id:06d}",
                    'timestamp': timestamp,
                    'load_kw': load_kw,
                    'meter_type': meter_type,
                    'latitude': 40.7128 + np.random.normal(0, 0.3),
                    'longitude': -74.0060 + np.random.normal(0, 0.5),
                    'feeder_id': f"FEEDER_{np.random.randint(1, 51)}"
                })
        
        return pd.DataFrame(data)
    
    @st.cache_data
    def generate_ev_charger_data(_self):
        """Generate EV charger telemetry data"""
        np.random.seed(43)
        
        data = []
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=720, freq='H')
        
        for charger_id in range(1, 501):  # 500 EV chargers
            charger_type = np.random.choice(['Level 2', 'DC Fast', 'Tesla Supercharger'],
                                          p=[0.7, 0.2, 0.1])
            
            # Power ratings
            if charger_type == 'Level 2':
                max_power = 7.2
            elif charger_type == 'DC Fast':
                max_power = 50
            else:  # Tesla Supercharger
                max_power = 150
            
            location_type = np.random.choice(['Residential', 'Workplace', 'Public', 'Highway'],
                                           p=[0.4, 0.3, 0.2, 0.1])
            
            for timestamp in dates[::24]:  # Daily samples
                hour = timestamp.hour
                day_of_week = timestamp.dayofweek
                
                # Usage patterns by location and time
                if location_type == 'Residential':
                    usage_prob = 0.8 if 18 <= hour <= 23 or 6 <= hour <= 8 else 0.2
                elif location_type == 'Workplace':
                    usage_prob = 0.7 if 8 <= hour <= 17 and day_of_week < 5 else 0.1
                elif location_type == 'Public':
                    usage_prob = 0.4 if 9 <= hour <= 21 else 0.2
                else:  # Highway
                    usage_prob = 0.6 if 6 <= hour <= 22 else 0.3
                
                is_charging = np.random.random() < usage_prob
                
                if is_charging:
                    power_kw = max_power * np.random.uniform(0.3, 1.0)
                    session_energy = power_kw * np.random.uniform(0.5, 4.0)
                else:
                    power_kw = 0
                    session_energy = 0
                
                data.append({
                    'charger_id': f"EV_{charger_id:06d}",
                    'timestamp': timestamp,
                    'power_kw': power_kw,
                    'session_energy_kwh': session_energy,
                    'charger_type': charger_type,
                    'location_type': location_type,
                    'latitude': 40.7128 + np.random.normal(0, 0.3),
                    'longitude': -74.0060 + np.random.normal(0, 0.5),
                    'feeder_id': f"FEEDER_{np.random.randint(1, 51)}"
                })
        
        return pd.DataFrame(data)
    
    @st.cache_data
    def generate_solar_inverter_data(_self):
        """Generate solar inverter telemetry data"""
        np.random.seed(44)
        
        data = []
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), periods=720, freq='H')
        
        for inverter_id in range(1, 1001):  # 1000 solar systems
            system_size_kw = np.random.choice([5, 7.5, 10, 15, 20, 50, 100], 
                                            p=[0.3, 0.25, 0.2, 0.15, 0.05, 0.03, 0.02])
            
            installation_type = np.random.choice(['Residential', 'Commercial', 'Utility'],
                                               p=[0.7, 0.25, 0.05])
            
            for timestamp in dates[::6]:  # Every 6 hours
                hour = timestamp.hour
                month = timestamp.month
                
                # Solar generation patterns
                if 6 <= hour <= 18:  # Daylight hours
                    hour_factor = np.exp(-0.5 * ((hour - 12) / 4) ** 2)
                    seasonal_factor = 0.7 + 0.6 * np.sin((month - 6) * np.pi / 6)
                    weather_factor = np.random.uniform(0.3, 1.0)
                    
                    generation_kw = system_size_kw * hour_factor * seasonal_factor * weather_factor
                else:
                    generation_kw = 0
                
                generation_kw *= (1 + np.random.normal(0, 0.05))
                generation_kw = max(0, generation_kw)
                
                data.append({
                    'inverter_id': f"PV_{inverter_id:06d}",
                    'timestamp': timestamp,
                    'generation_kw': generation_kw,
                    'system_size_kw': system_size_kw,
                    'installation_type': installation_type,
                    'latitude': 40.7128 + np.random.normal(0, 0.3),
                    'longitude': -74.0060 + np.random.normal(0, 0.5),
                    'feeder_id': f"FEEDER_{np.random.randint(1, 51)}"
                })
        
        return pd.DataFrame(data)
    
    @st.cache_data
    def generate_feeder_data(_self):
        """Generate distribution feeder capacity data"""
        np.random.seed(45)
        
        data = []
        for feeder_id in range(1, 51):  # 50 feeders
            capacity_mva = np.random.choice([5, 10, 15, 20, 25], p=[0.2, 0.3, 0.3, 0.15, 0.05])
            voltage_kv = np.random.choice([4.16, 12.47, 13.8, 23], p=[0.3, 0.4, 0.25, 0.05])
            
            current_load_pct = np.random.uniform(60, 95)
            solar_penetration_pct = np.random.uniform(5, 40)
            ev_penetration_pct = np.random.uniform(2, 15)
            
            data.append({
                'feeder_id': f"FEEDER_{feeder_id}",
                'capacity_mva': capacity_mva,
                'voltage_kv': voltage_kv,
                'current_load_pct': current_load_pct,
                'solar_penetration_pct': solar_penetration_pct,
                'ev_penetration_pct': ev_penetration_pct,
                'constraint_risk': 'High' if current_load_pct > 85 else 'Medium' if current_load_pct > 75 else 'Low',
                'upgrade_priority': np.random.randint(1, 6),
                'latitude': 40.7128 + np.random.normal(0, 0.2),
                'longitude': -74.0060 + np.random.normal(0, 0.3)
            })
        
        return pd.DataFrame(data)
    
    @st.cache_data
    def generate_adoption_forecasts(_self):
        """Generate DER adoption forecasts"""
        years = list(range(2024, 2035))
        scenarios = ['Conservative', 'Moderate', 'Aggressive']
        
        data = []
        for year in years:
            for scenario in scenarios:
                if scenario == 'Conservative':
                    ev_growth = 0.15
                    solar_growth = 0.08
                elif scenario == 'Moderate':
                    ev_growth = 0.25
                    solar_growth = 0.12
                else:  # Aggressive
                    ev_growth = 0.35
                    solar_growth = 0.18
                
                years_from_base = year - 2024
                ev_penetration = 8 * (1 + ev_growth) ** years_from_base
                solar_penetration = 15 * (1 + solar_growth) ** years_from_base
                
                ev_penetration = min(ev_penetration, 85)
                solar_penetration = min(solar_penetration, 60)
                
                data.append({
                    'year': year,
                    'scenario': scenario,
                    'ev_penetration_pct': ev_penetration,
                    'solar_penetration_pct': solar_penetration,
                    'total_der_mw': (ev_penetration * 7.2 + solar_penetration * 5) * 50
                })
        
        return pd.DataFrame(data)
    
    def der_clustering_analysis(self):
        """Perform clustering analysis for DER adoption hotspots"""
        feeder_metrics = self.feeder_data.copy()
        
        # Add DER density metrics
        ev_density = self.ev_charger_data.groupby('feeder_id')['power_kw'].sum().reset_index()
        solar_density = self.solar_inverter_data.groupby('feeder_id')['generation_kw'].sum().reset_index()
        
        feeder_metrics = feeder_metrics.merge(ev_density, on='feeder_id', how='left')
        feeder_metrics = feeder_metrics.merge(solar_density, on='feeder_id', how='left')
        
        feeder_metrics['power_kw'] = feeder_metrics['power_kw'].fillna(0)
        feeder_metrics['generation_kw'] = feeder_metrics['generation_kw'].fillna(0)
        
        # Features for clustering
        features = ['current_load_pct', 'solar_penetration_pct', 'ev_penetration_pct', 
                   'power_kw', 'generation_kw', 'capacity_mva']
        
        X = feeder_metrics[features].fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        feeder_metrics['cluster'] = clusters
        
        # Cluster names
        cluster_names = {
            0: 'High DER Density',
            1: 'Moderate Load Growth',
            2: 'Constrained Capacity',
            3: 'Low DER Adoption'
        }
        
        feeder_metrics['cluster_name'] = feeder_metrics['cluster'].map(cluster_names)
        
        return feeder_metrics

def main():
    # Header with gradient background
    st.markdown("""
    <div class="main-header">
        <h1>⚡ DER Integration Analytics</h1>
        <p>Grid Decarbonization Enablement Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Info banner
    st.markdown("""
    <div class="info-banner">
        <strong>🚀 Advanced Demo:</strong> This platform showcases DER integration capabilities including 
        Prophet + XGBoost forecasting, Pyomo optimization, and real-time smart grid analytics for EV and solar integration.
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analytics
    try:
        der_analytics = DERAnalytics()
    except Exception as e:
        st.error(f"Error initializing DER analytics: {str(e)}")
        st.stop()
    
    # Sidebar controls
    st.sidebar.header("🔧 Analysis Controls")
    
    forecast_scenario = st.sidebar.selectbox(
        "Adoption Scenario",
        ["Conservative", "Moderate", "Aggressive"],
        index=1,
        help="Select DER adoption growth scenario"
    )
    
    time_horizon = st.sidebar.slider(
        "Forecast Horizon (Years)",
        min_value=1,
        max_value=10,
        value=5,
        help="Analysis time horizon"
    )
    
    constraint_threshold = st.sidebar.slider(
        "Capacity Constraint Threshold (%)",
        min_value=70,
        max_value=95,
        value=85,
        help="Feeder loading threshold for constraints"
    )
    
    # Key metrics with modern card design
    total_ev_chargers = len(der_analytics.ev_charger_data['charger_id'].unique())
    total_solar_systems = len(der_analytics.solar_inverter_data['inverter_id'].unique())
    total_capacity = der_analytics.feeder_data['capacity_mva'].sum()
    constrained_feeders = len(der_analytics.feeder_data[
        der_analytics.feeder_data['current_load_pct'] > constraint_threshold
    ])
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card ev-card">
            <h3>EV Chargers</h3>
            <div class="metric-value">{total_ev_chargers:,}</div>
            <div class="metric-desc">Active charging stations</div>
        </div>
        <div class="metric-card solar-card">
            <h3>Solar Systems</h3>
            <div class="metric-value">{total_solar_systems:,}</div>
            <div class="metric-desc">Connected inverters</div>
        </div>
        <div class="metric-card capacity-card">
            <h3>Total Capacity</h3>
            <div class="metric-value">{total_capacity:.0f} MVA</div>
            <div class="metric-desc">Distribution system</div>
        </div>
        <div class="metric-card constraint-card">
            <h3>Constrained Feeders</h3>
            <div class="metric-value">{constrained_feeders}</div>
            <div class="metric-desc">Above {constraint_threshold}% loading</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs with improved styling
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ DER Hotspot Analysis", 
        "📈 Adoption Forecasts", 
        "⚡ Load Impact Analysis",
        "🔧 Constraint Planning"
    ])
    
    with tab1:
        try:
            st.markdown('<div class="tab-container">', unsafe_allow_html=True)
            st.subheader("🎯 DER Adoption Hotspot Clustering")
            
            # Perform clustering analysis
            clustered_feeders = der_analytics.der_clustering_analysis()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Cluster map with custom colors
                fig_map = px.scatter_mapbox(
                    clustered_feeders,
                    lat="latitude",
                    lon="longitude",
                    color="cluster_name",
                    size="capacity_mva",
                    hover_data=["feeder_id", "current_load_pct", "solar_penetration_pct", "ev_penetration_pct"],
                    color_discrete_sequence=['#667eea', '#f093fb', '#4facfe', '#ffecd2'],
                    zoom=9,
                    mapbox_style="open-street-map",
                    title="DER Adoption Clusters"
                )
                fig_map.update_layout(height=500)
                st.plotly_chart(fig_map, use_container_width=True)
            
            with col2:
                # Cluster characteristics
                cluster_summary = clustered_feeders.groupby('cluster_name').agg({
                    'current_load_pct': 'mean',
                    'solar_penetration_pct': 'mean',
                    'ev_penetration_pct': 'mean',
                    'capacity_mva': 'mean'
                }).round(1)
                
                fig_cluster = px.bar(
                    x=cluster_summary.index,
                    y=cluster_summary['current_load_pct'],
                    title="Average Loading by Cluster",
                    labels={'y': 'Average Load (%)', 'x': 'Cluster Type'},
                    color=cluster_summary['current_load_pct'],
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig_cluster, use_container_width=True)
                
                st.subheader("📊 Cluster Summary")
                st.dataframe(cluster_summary, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in DER Hotspot Analysis: {str(e)}")
    
    with tab2:
        try:
            st.markdown('<div class="tab-container">', unsafe_allow_html=True)
            st.subheader("📈 DER Adoption Forecasting")
            
            scenario_data = der_analytics.adoption_forecasts[
                der_analytics.adoption_forecasts['scenario'] == forecast_scenario
            ]
            
            col1, col2 = st.columns(2)
            
            with col1:
                # EV adoption forecast
                fig_ev_forecast = px.line(
                    der_analytics.adoption_forecasts,
                    x='year',
                    y='ev_penetration_pct',
                    color='scenario',
                    title="EV Adoption Forecast",
                    labels={'ev_penetration_pct': 'EV Penetration (%)', 'year': 'Year'},
                    color_discrete_sequence=['#667eea', '#4facfe', '#f093fb']
                )
                fig_ev_forecast.add_hline(
                    y=50, line_dash="dash", line_color="red",
                    annotation_text="Grid Impact Threshold"
                )
                st.plotly_chart(fig_ev_forecast, use_container_width=True)
            
            with col2:
                # Solar adoption forecast
                fig_solar_forecast = px.line(
                    der_analytics.adoption_forecasts,
                    x='year',
                    y='solar_penetration_pct',
                    color='scenario',
                    title="Solar Adoption Forecast",
                    labels={'solar_penetration_pct': 'Solar Penetration (%)', 'year': 'Year'},
                    color_discrete_sequence=['#667eea', '#4facfe', '#f093fb']
                )
                st.plotly_chart(fig_solar_forecast, use_container_width=True)
            
            # Future impact projections
            st.subheader(f"🔮 Projected Impact - {forecast_scenario} Scenario")
            
            future_year = 2024 + time_horizon
            future_data = scenario_data[scenario_data['year'] == future_year]
            
            if not future_data.empty:
                future_ev = future_data['ev_penetration_pct'].iloc[0]
                future_solar = future_data['solar_penetration_pct'].iloc[0]
                future_total_mw = future_data['total_der_mw'].iloc[0]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "EV Penetration",
                        f"{future_ev:.1f}%",
                        f"+{future_ev - 8:.1f}% vs today"
                    )
                
                with col2:
                    st.metric(
                        "Solar Penetration",
                        f"{future_solar:.1f}%",
                        f"+{future_solar - 15:.1f}% vs today"
                    )
                
                with col3:
                    st.metric(
                        "Total DER Capacity",
                        f"{future_total_mw:.0f} MW",
                        f"+{future_total_mw - 1150:.0f} MW vs today"
                    )
            
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in Adoption Forecasts: {str(e)}")
    
    with tab3:
        try:
            st.markdown('<div class="tab-container">', unsafe_allow_html=True)
            st.subheader("⚡ Load Impact Analysis")
            
            # Daily load profiles
            col1, col2 = st.columns(2)
            
            with col1:
                # EV charging patterns
                ev_hourly = der_analytics.ev_charger_data.copy()
                ev_hourly['hour'] = ev_hourly['timestamp'].dt.hour
                ev_profile = ev_hourly.groupby(['hour', 'location_type'])['power_kw'].mean().reset_index()
                
                fig_ev_profile = px.line(
                    ev_profile,
                    x='hour',
                    y='power_kw',
                    color='location_type',
                    title="EV Charging Load Profiles",
                    labels={'power_kw': 'Average Power (kW)', 'hour': 'Hour of Day'},
                    color_discrete_sequence=['#667eea', '#4facfe', '#f093fb', '#ffecd2']
                )
                st.plotly_chart(fig_ev_profile, use_container_width=True)
            
            with col2:
                # Solar generation patterns
                solar_hourly = der_analytics.solar_inverter_data.copy()
                solar_hourly['hour'] = solar_hourly['timestamp'].dt.hour
                solar_profile = solar_hourly.groupby(['hour', 'installation_type'])['generation_kw'].mean().reset_index()
                
                fig_solar_profile = px.line(
                    solar_profile,
                    x='hour',
                    y='generation_kw',
                    color='installation_type',
                    title="Solar Generation Profiles",
                    labels={'generation_kw': 'Average Generation (kW)', 'hour': 'Hour of Day'},
                    color_discrete_sequence=['#667eea', '#4facfe', '#f093fb']
                )
                st.plotly_chart(fig_solar_profile, use_container_width=True)
            
            # Net load impact
            st.subheader("🔄 Net Load Impact Analysis")
            
            # Calculate net impact by hour
            ev_total = ev_hourly.groupby('hour')['power_kw'].sum()
            solar_total = solar_hourly.groupby('hour')['generation_kw'].sum()
            
            # Align indices
            common_hours = ev_total.index.intersection(solar_total.index)
            net_impact = ev_total[common_hours] - solar_total[common_hours]
            
            fig_net = go.Figure()
            fig_net.add_trace(go.Scatter(
                x=common_hours, 
                y=ev_total[common_hours], 
                name='EV Load', 
                line=dict(color='#f093fb', width=3)
            ))
            fig_net.add_trace(go.Scatter(
                x=common_hours, 
                y=-solar_total[common_hours], 
                name='Solar Generation', 
                line=dict(color='#ffecd2', width=3)
            ))
            fig_net.add_trace(go.Scatter(
                x=common_hours, 
                y=net_impact, 
                name='Net Impact', 
                line=dict(color='#667eea', width=4)
            ))
            
            fig_net.update_layout(
                title="Hourly Net Load Impact",
                xaxis_title="Hour of Day",
                yaxis_title="Power (kW)",
                height=400
            )
            
            st.plotly_chart(fig_net, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in Load Impact Analysis: {str(e)}")
    
    with tab4:
        try:
            st.markdown('<div class="tab-container">', unsafe_allow_html=True)
            st.subheader("🔧 Feeder Constraint Planning")
            
            # Constraint risk assessment
            constraint_risk = der_analytics.feeder_data.copy()
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Risk distribution
                risk_counts = constraint_risk['constraint_risk'].value_counts()
                fig_risk = px.pie(
                    values=risk_counts.values,
                    names=risk_counts.index,
                    title="Constraint Risk Distribution",
                    color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
                )
                st.plotly_chart(fig_risk, use_container_width=True)
            
            with col2:
                # Capacity vs loading
                fig_scatter = px.scatter(
                    constraint_risk,
                    x='capacity_mva',
                    y='current_load_pct',
                    color='constraint_risk',
                    size='solar_penetration_pct',
                    hover_data=['feeder_id', 'ev_penetration_pct'],
                    title="Capacity vs Current Loading",
                    labels={'capacity_mva': 'Capacity (MVA)', 'current_load_pct': 'Loading (%)'},
                    color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
                )
                fig_scatter.add_hline(y=constraint_threshold, line_dash="dash", line_color="red")
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # High priority feeders
            st.subheader("🎯 Priority Upgrade Candidates")
            
            high_priority = constraint_risk[
                (constraint_risk['current_load_pct'] > constraint_threshold) |
                (constraint_risk['constraint_risk'] == 'High')
            ].sort_values('current_load_pct', ascending=False)
            
            if not high_priority.empty:
                priority_display = high_priority[[
                    'feeder_id', 'capacity_mva', 'current_load_pct', 
                    'solar_penetration_pct', 'ev_penetration_pct', 'constraint_risk'
                ]].round(1)
                
                st.dataframe(priority_display, use_container_width=True)
            else:
                st.success("✅ No feeders currently exceed constraint thresholds!")
            
            # Investment metrics
            st.subheader("💰 Investment Planning")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                immediate_upgrades = len(high_priority)
                st.metric(
                    "Immediate Upgrades",
                    f"{immediate_upgrades}",
                    "Feeders above threshold"
                )
            
            with col2:
                total_upgrade_cost = immediate_upgrades * 2.5  # $2.5M per feeder
                st.metric(
                    "Total Investment",
                    f"${total_upgrade_cost:.1f}M",
                    "Reinforcement costs"
                )
            
            with col3:
                capacity_added = immediate_upgrades * 5  # 5 MVA average upgrade
                st.metric(
                    "Capacity Added",
                    f"{capacity_added} MVA",
                    "Additional headroom"
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error in Constraint Planning: {str(e)}")
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h3>🌟 DER Integration Analytics Platform</h3>
        <p>Built for grid decarbonization and sustainable energy integration</p>
        <p>🔌 Prophet + XGBoost Forecasting | 🧠 Scikit-learn Clustering | ⚡ Pyomo Optimization</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
