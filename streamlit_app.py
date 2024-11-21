# Import required libraries
import pandas as pd            # Data manipulation library
import streamlit as st          # Web application framework for creating interactive dashboards

# Configure Streamlit page settings
st.set_page_config(
    page_title="Analytics Dashboard",   # Set the title of the browser tab
    page_icon="📊",               # Set a chart emoji as the page icon
    layout="wide",               # Use wide layout to maximize screen space
)

# Set the logo for the application
st.logo("./img/round_analytics.png")

# Initialize session state for storing application options
# This ensures that certain variables persist across page reloads
if "options" not in st.session_state:
    st.session_state.options = None

# Define pages for multi-page Streamlit application

# Analytics Dashboard page
# Links to the analytics.py script
analytics_page = st.Page(
    "./app/analytics.py",       # Path to the Python script for this page
    title="Analytics Dashboard"  # Title displayed in the navigation menu
)

# AI/ML Implementation page
# Links to the ai_implementation.py script
ai_page = st.Page(
    "./app/ai_implementation.py",
    title="AI/ML Implementation", 
)

# Raw Data View page
# Links to the view_data.py script
data_page = st.Page(
    "./app/view_data.py",
    title="Raw Data", 
)

# Create navigation menu with defined pages
# Allows user to switch between different pages of the application
selected_page = st.navigation([
    analytics_page,   # Analytics Dashboard page
    ai_page,          # AI/ML Implementation page
    data_page         # Raw Data page
])

# Run the selected page
# This will load and execute the Python script for the page the user has selected
selected_page.run()