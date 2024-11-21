# Import required libraries
import streamlit as st           # Web application framework
import pandas as pd              # Data manipulation and analysis
import plotly.express as px      # Interactive data visualization

# Function to load AI analysis results from CSV
def load_ai_results():
    # Read the CSV file containing anomaly detection results
    data = pd.read_csv("data/ai_results.csv")
    return data

# Set the title of the Streamlit web application
st.title("Anomaly Detection in Network Data")

# Create an expandable section explaining the approach
with st.expander("See Approach to Solution"):
    # Markdown text detailing the anomaly detection methodology
    st.markdown("""
    ## Approach to Solution

    ### 1. Data Preparation
    I started with a dataset containing network routing information, including features like LocPrf and Hop Count. The data was cleaned and filtered to include relevant metrics and paths.

    ### 2. Feature Selection
    The features selected for analysis were:
    - **LocPrf (Local Preference)**: Indicates the preference for a route within an Autonomous System (AS).
    - **Hop Count**: Shows the number of ASNs a route has traversed.

    ### 3. Anomaly Detection Using Isolation Forest
    #### Model Selection and Training
    I employed the Isolation Forest model for unsupervised anomaly detection. The model parameters were fine-tuned to achieve optimal performance:
    - **n_estimators = 25**: The number of base estimators in the ensemble.
    - **max_samples = 'auto'**: The number of samples to draw from the dataset to train each base estimator.
    - **contamination = 0.0015**: The proportion of outliers in the dataset.
    - **random_state = 42**: Ensures reproducibility of the results.

    #### Anomaly Detection Process
    - **Model Training**: The Isolation Forest model was trained using the selected features `LocPrf` and `hop_count`.
    - **Prediction**: The model was used to predict anomalies in the dataset. Data points were labeled as 'Anomaly' if they significantly deviated from the norm.

    ### 4. Analysis and Visualization
    Anomalies were analyzed by examining the distribution across different features. I created interactive visualizations to highlight patterns and potential issues:
    - **Plotly Scatter Plot**: An interactive scatter plot was generated to visualize the distribution of anomalies against normal data points:
      - **X-axis**: Hop Count
      - **Y-axis**: Local Preference
      - **Color Coding**: Anomalies were highlighted in red, and normal data points were shown in blue.

    ### 5. Results
    The detected anomalies were saved to a CSV file for further analysis and reporting. This systematic approach ensures comprehensive analysis and accurate detection of anomalies in the network data.

    This comprehensive approach ensures accurate detection and effective visualization of anomalies in network routing data, providing valuable insights for maintaining and improving network performance.
    """)

# Load the AI results data
df = load_ai_results()

# Display data cleaning information
st.write("Data Cleaning:")
st.write("\t1. Only Data with IP prefixes from transit providers is considered")
st.write("\t2. Data with null Metric values where removed")

# Display total number of prefixes after cleaning
st.write(f" Total Number of prefixes after data cleaning: *{len(df)}*")

# Filter and count normal prefixes
normal_prefixes = df[df['Anomaly'] == 'Normal']
st.write(f" Normal Prefixes: *{len(normal_prefixes)}*")

# Filter and count anomalous prefixes
anomalous_prefixes = df[df['Anomaly'] == 'Anomaly']
st.write(f" Anomalous Prefixes: *{len(anomalous_prefixes)}*")

# Add a subheader for results
st.subheader("_Results_")

# Create first interactive scatter plot: Hop Count vs LocPrf
fig = px.scatter(df, x='hop_count', y='LocPrf', color='Anomaly',
                 # Color mapping for anomaly and normal data points
                 color_discrete_map={'Anomaly': 'red', 'Normal': 'blue'},
                 # Custom labels for axes and legend
                 labels={'Next Hop': 'Next Hop', 'Metric': 'Metric', 'LocPrf': 'LocPrf', 'hop_count': 'Hop Count', 'Anomaly': 'Data Type'},
                 title='Anomaly vs. Normal Data Points')

# Update legend title
fig.update_layout(legend_title_text='Data Type')

# Display the first Plotly figure in Streamlit
st.plotly_chart(fig)

# Create second interactive scatter plot: Hop Count vs Transit AS
fig = px.scatter(df, x='hop_count', y='transit_as', color='Anomaly',
                 # Color mapping for anomaly and normal data points
                 color_discrete_map={'Anomaly': 'red', 'Normal': 'blue'},
                 # Custom labels for axes
                 labels={'transit_as': 'Transit AS', 'hop_count': 'Hop Count'},
                 title='Anomaly vs. Normal Data Points')

# Update legend title
fig.update_layout(legend_title_text='Data Type')

# Display the second Plotly figure in Streamlit
st.plotly_chart(fig)

# Add a subheader for tabular view
st.subheader("Anomaly Detection Results - _Tabular View_ ")

# Display the entire DataFrame
st.dataframe(df)