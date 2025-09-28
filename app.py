import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="DER Test", page_icon="⚡", layout="wide")

st.title("⚡ DER Integration Analytics - Test Version")

st.success("✅ App is working! All dependencies loaded successfully.")

# Simple test data
data = pd.DataFrame({
    'x': range(10),
    'y': np.random.randn(10)
})

fig = px.line(data, x='x', y='y', title="Test Chart")
st.plotly_chart(fig)

st.info("If you see this, the basic app is working. You can now replace with the full version.")
