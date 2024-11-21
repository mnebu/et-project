# Import necessary libraries
import pandas as pd              # Data manipulation and analysis
import plotly.express as px      # Interactive data visualization
import streamlit as st           # Web app framework for data apps
import plotly.graph_objects as go # Advanced plotting capabilities
import io

#################################################
### DATA LOADING
#################################################
# Cached function to load data efficiently
# @st.cache_data ensures the data is loaded only once and reused
@st.cache_data(max_entries=5)
def load_data():
    # Read the CSV file containing IP prefix data
    data = pd.read_csv("data/data.csv")
    return data

#################################################
### USER INTERFACE SETUP
#################################################
# Set the title of the Streamlit web application
st.title("📊 BGP IP Prefixes Analytics")

# Load the data
IPV4_IPV6_df = load_data()

# Separate IPv4 and IPv6 networks based on address format
# IPv4 addresses contain dots (.)
IPV4_df = IPV4_IPV6_df[IPV4_IPV6_df['Network'].str.contains(r'\.', regex=True)]
# IPv6 addresses contain colons (:)
IPV6_df = IPV4_IPV6_df[IPV4_IPV6_df['Network'].str.contains(r'\:', regex=True)]

# Read transit Autonomous System (AS) numbers from a text file
# These are specific network provider AS numbers
with open('./data/transitASN.txt', 'r') as file:
    transit_as_numbers = [int(line.strip()) for line in file]

# Filter dataframes to include only transit provider networks
transit_IPV4_df = IPV4_df[IPV4_df['transit_as'].isin(transit_as_numbers)]
transit_IPV6_df = IPV6_df[IPV6_df['transit_as'].isin(transit_as_numbers)]

# Calculate various prefix count metrics
count_number_ipv4_ipv6_prefixes = len(IPV4_IPV6_df)     # Total IP prefixes
count_number_ipv4_prefixes = len(IPV4_df)               # Total IPv4 prefixes
count_number_ipv6_prefixes = len(IPV6_df)               # Total IPv6 prefixes
count_number_ipv4_transit_prefixes = len(transit_IPV4_df)  # IPv4 prefixes from transit providers
count_number_ipv6_transit_prefixes = len(transit_IPV6_df)  # IPv6 prefixes from transit providers

# Total transit provider prefixes
count_number_ipv4_ipv6_transit_prefixes = count_number_ipv4_transit_prefixes + count_number_ipv6_transit_prefixes

# Create three-column layout for high-level metrics
row_metrics = st.columns(3)

# Display total number of IP prefixes in the first column
with row_metrics[0]:
    with st.container(border=True):
        st.metric(
            "Total Number of IP Prefixes",
            f"{count_number_ipv4_ipv6_prefixes:,}",  # Format with comma separator
        )

# Display total number of IPv4 prefixes in the second column
with row_metrics[1]:
    with st.container(border=True):
        st.metric(
            "Total Number of IPV4 Prefixes",
            f"{count_number_ipv4_prefixes:,}",  # Format with comma separator
        )

# Display total number of IPv6 prefixes in the third column
with row_metrics[2]:
    with st.container(border=True):
        st.metric(
            "Total Number of IPV6 Prefixes",
            f"{count_number_ipv6_prefixes:,}",  # Format with comma separator
        )

# Define color scheme for visualizations
colors = ['#FFD700', '#1E90FF']

# Add descriptive text
st.text("IP prefixes coming from transit providers versus external providers - Visualization")

# Create three-column layout for pie charts
pie_chart_metrics = st.columns(3)

# First pie chart: Overall IPv4 and IPv6 transit vs non-transit prefixes
with pie_chart_metrics[0]:
    with st.container():
        values = [count_number_ipv4_ipv6_transit_prefixes, count_number_ipv4_ipv6_prefixes - count_number_ipv4_ipv6_transit_prefixes]
        fig = go.Figure(data=[go.Pie(labels=['IPV4 and IPV6 prefixes coming from transit providers', 'Other IPV4 and IPV6 prefixes'], values=values, hole=.3, marker=dict(colors=colors), showlegend=True, textinfo='value')])
        fig.update_layout(title_text='IPV4 and IPV6', title_x=0.35, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig)

# Second pie chart: IPv4 transit vs non-transit prefixes
with pie_chart_metrics[1]:
    with st.container():
        values = [count_number_ipv4_transit_prefixes, count_number_ipv4_prefixes - count_number_ipv4_transit_prefixes]
        fig = go.Figure(data=[go.Pie(labels=['IPV4 prefixes coming from transit providers', 'Other IPV4 prefixes'], values=values, hole=.3, marker=dict(colors=colors), showlegend=True, textinfo='value')])
        fig.update_layout(title_text='IPV4', title_x=0.45, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig)

# Third pie chart: IPv6 transit vs non-transit prefixes
with pie_chart_metrics[2]:
    with st.container():
        values = [count_number_ipv6_transit_prefixes, count_number_ipv6_prefixes - count_number_ipv6_transit_prefixes]
        fig = go.Figure(data=[go.Pie(labels=['IPV6 prefixes coming from transit providers', 'Other IPV6 prefixes'], values=values, hole=.3, marker=dict(colors=colors), showlegend=True, textinfo='value')])
        fig.update_layout(title_text='IPV6', title_x=0.45, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig)

# Analyze hop count distribution
# Count the number of IP prefixes for each hop count
hop_count_distribution = IPV4_IPV6_df['hop_count'].value_counts().sort_index()

# Convert hop count distribution to a DataFrame for better visualization
hop_count_df = hop_count_distribution.reset_index()
hop_count_df.columns = ['No. of Hops', 'Count of IP Prefixes']

# Remove the first row (likely representing 0 hops)
hop_count_df = hop_count_df.iloc[1:, :]

# Create bar chart of IP prefixes by number of hops
fig = px.bar(hop_count_df, x='No. of Hops', y='Count of IP Prefixes',
             labels={'No. of Hops': 'No. of Hops', 'Count of IP Prefixes': 'Count of IP Prefixes'},
             title="Count of IP Prefixes by Number of Hops")
st.plotly_chart(fig)

# Display hop count distribution as a table
st.subheader("Count of IP Prefixes by Number of Hops - _Tabular View_ ")
st.table(hop_count_df)

# Expandable section for basic data analysis
with st.expander("Basic Data Analysis"):
    # Display the shape of the DataFrame (rows and columns)
    st.subheader('DataFrame Shape')
    st.write(IPV4_IPV6_df.shape)

    # Redirect the output of IPV4_IPV6_df.info() to a string 
    buffer = io.StringIO() 
    IPV4_IPV6_df.info(buf=buffer) 
    s = buffer.getvalue() 
    # Print the string in Streamlit 
    st.text(s)

    # Check for missing values
    st.subheader('Missing Values')
    st.table(IPV4_IPV6_df.isnull().sum())

    # Display descriptive statistics
    st.subheader('Descriptive Statistics')
    st.table(IPV4_IPV6_df.describe())