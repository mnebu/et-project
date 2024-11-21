# Import required libraries
import streamlit as st           # Web application framework
import pandas as pd              # Data manipulation and analysis
import mysql.connector           # MySQL database connector
from mysql.connector import errorcode  # Error handling for MySQL connections

# Cached function to load data from CSV
# @st.cache_data ensures the data is loaded efficiently and cached
@st.cache_data(max_entries=5)
def load_data():
    # Read the CSV file
    data = pd.read_csv("data/data.csv")
    
    # Select and return only the first 6 columns of the DataFrame
    return data.iloc[:, :6]

# Commented-out alternative function to load data directly from MySQL database
# Kept as a reference for potential future database connectivity
# @st.cache_data(max_entries=5)
# def load_data(query: str):
#     # Database configuration dictionary
#     config = {
#         'host':'mysql-server.mysql.database.azure.com',
#         'user':'AzureAdminNebuhan',
#         'password':'86',
#         'database':'etisalat_project'
#     }
# 
#     # Attempt to establish database connection
#     try:
#         sql_connection = mysql.connector.connect(**config)
#         print("Connection established")
#     except mysql.connector.Error as err:
#         # Handle potential connection errors
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with the user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)
# 
#     # Execute SQL query and load results into a pandas DataFrame
#     data = pd.read_sql(
#         query,
#         sql_connection
#     )
# 
#     return data

# Set the header for the Streamlit application
st.header("🛢️ Raw Data as in Database")

# Load the data using the defined function
IPV4_IPV6_df = load_data()

# Display the loaded DataFrame in the Streamlit app
st.dataframe(IPV4_IPV6_df)

# Create a detailed markdown section explaining the data extraction approach
st.markdown("""
# Data Extraction and Insertion Approach

## Task 1: Data Extraction

**Problem:** 
Extract data from the .rr files, which contain command-line output, into a structured format suitable for insertion into a MySQL database.

**Initial Attempts:**
I initially tried using pandas libraries like `read_csv()` and `read_fwf()`, among other tools, to extract the tabular data directly. However, these tools partially parsed the data, and the required format wasn't achieved.

**Solution:**
Due to the inadequacy of the existing tools, I wrote a custom Python program to accurately parse each line from the file and retrieve the necessary data. The program then adds this data to the database.

## Approach

1. **File Processing:**
    - Opened the BGP routing table files (`typescript.IPV4.RR` and `typescript.IPV6.RR`).
    - Read each line, identifying route entries indicated by lines starting with "*".
    - Concatenated multiline entries for complete parsing.
    
2. **Data Extraction:**
    - Extracted essential BGP attributes:
        - Network prefix
        - Next hop address
        - BGP metric (handled missing metrics with conditional checks)
        - Local preference
        - Weight
        - AS path
    - Ensured accurate data extraction even for entries split across multiple lines.

3. **Database Insertion:**
    - Prepared the extracted data in a tuple format for insertion.
    - Used parameterized SQL queries to safely insert data into the MySQL database.
    - Committed the transactions and closed database connections after insertion.

## Result

The custom script successfully extracted the required data and populated the MySQL database. This approach ensured that all necessary information was accurately retrieved and stored.

## Conclusion

This approach ensured precise extraction and insertion of routing data into the MySQL database, addressing the issues faced with pre-built libraries and tools.

## Code

Here's a snippet of the Python code used to achieve this:

```python
# Import required MySQL connector for database operations
import mysql.connector

# Establish database connection with MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Fg3*d12",
  database="etisalat_project"
)

# Create a cursor object to execute SQL queries
mycursor = mydb.cursor()

# Prepare SQL query with parameterized values for safe insertion
sql_query = "INSERT INTO ipv4_ipv6 (Network, NextHop, Metric, LocPrf, Weight, Path) VALUES (%s, %s, %s, %s, %s, %s)"

# Initialize counter for tracking number of inserted records
count = 0

# Input file path - Comment/uncomment appropriate file based on IP version needed
#file_name = 'data_file/typescript.IPV4.RR/typescript.IPV4.RR.txt'
file_name = 'data_file/typescript.IPV6.RR/typescript.IPV6.RR.txt'

# Open and process the BGP routing table file
with open(file_name, "r") as file:

    for line in file:
        # Check if line starts with "*" indicating a new route entry
        if line.startswith("*"):
            parsed_line = ""  # Initialize variable for storing complete route entry
            parsed_line = line.strip()  # Store the first line of route entry
        # Check if line starts with space indicating continuation of previous entry
        elif line.startswith(" "):
            parsed_line += " " + line.strip()  # Append continuation line to current entry
        parsed_line.split()
        
        # Process only valid route entries (length > 50 chars)
        if len(parsed_line) > 50:
            # Initialize variables for storing BGP attributes
            network = ""    # Store network prefix
            next_hop = ""   # Store next hop address
            metric = ""     # Store BGP metric
            locprf = ""     # Store local preference
            weight = ""     # Store weight
            path = ""       # Store AS path

            # Parsing logic for extracting different BGP attributes
            # (Detailed parsing logic as in the original code)
            ...

# Commit all database insertions
mydb.commit()
print(count, "record inserted.")

# Clean up database connections
mycursor.close()
mydb.close()
```
            """)