import streamlit as st
import pandas as pd
import plotly.express as px

def load_ai_results():
    data = pd.read_csv("data/ai_results.csv")
    return data

# Title of the app
st.title("Anomaly Detection in Network Data")

# Description of the approach inside an expander
with st.expander("See Approach to Solution"):
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


# Read the CSV file into a DataFrame
df = load_ai_results()

st.write("Data Cleaning:")
st.write("\t1. Only Data with IP prefixes from transit providers is considered")
st.write("\t2. Data with null Metric values where removed")

st.write(f" Total Number of prefixes after data cleaning: *{len(df)}*")

normal_prefixes = df[df['Anomaly'] == 'Normal']
st.write(f" Normal Prefixes: *{len(normal_prefixes)}*")

anomalous_prefixes = df[df['Anomaly'] == 'Anomaly']
st.write(f" Anomalous Prefixes: *{len(anomalous_prefixes)}*")

st.subheader("_Results_")

# Create an interactive scatter plot
fig = px.scatter(df, x='hop_count', y='LocPrf', color='Anomaly',
                 color_discrete_map={'Anomaly': 'red', 'Normal': 'blue'},
                 labels={'Next Hop': 'Next Hop', 'Metric': 'Metric', 'LocPrf': 'LocPrf', 'hop_count': 'Hop Count', 'Anomaly': 'Data Type'},
                 title='Anomaly vs. Normal Data Points')

# Update legend titles
fig.update_layout(legend_title_text='Data Type')

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)


# Create an interactive scatter plot
fig = px.scatter(df, x='hop_count', y='transit_as', color='Anomaly',
                 color_discrete_map={'Anomaly': 'red', 'Normal': 'blue'},
                 labels={'transit_as': 'Transit AS', 'hop_count': 'Hop Count'},
                 title='Anomaly vs. Normal Data Points')

# Update legend titles
fig.update_layout(legend_title_text='Data Type')

# Display the Plotly figure in Streamlit
st.plotly_chart(fig)

st.subheader("Anomaly Detection Results - _Tabular View_ ")

# Display the DataFrame
st.dataframe(df)
