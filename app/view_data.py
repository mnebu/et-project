import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import errorcode

@st.cache_data(max_entries=5)
def load_data():
    data = pd.read_csv("data/data.csv")
    # Select the first five columns
    return data.iloc[:, :6]

# Uncomment following code to read data from MySQL Database. Make appropriate changes to the config credentials.
# @st.cache_data(max_entries=5)
# def load_data(query: str):
#     # Function to get data from MySQL
#     config = {
#         'host':'mysql-server.mysql.database.azure.com',
#         'user':'AzureAdminNebuhan',
#         'password':'86',
#         'database':'etisalat_project'
#     }

#     # Construct connection string

#     try:
#         sql_connection = mysql.connector.connect(**config)
#         print("Connection established")
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Something is wrong with the user name or password")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database does not exist")
#         else:
#             print(err)

#     data = pd.read_sql(
#         query,
#         sql_connection
#     )

#     return data

st.header("🛢️ Raw Data as in Database")

IPV4_IPV6_df = load_data()

st.dataframe(IPV4_IPV6_df)

st.markdown("""
# Data Extraction and Insertion Approach

## Task 1: Data Extraction

**Problem:** 
Extract data from the .rr files, which contain command-line output, into a structured format suitable for insertion into a MySQL database.

**Initial Attempts:**
I initially tried using pandas libraries like `read_csv()` and `read_fwf()`, among other tools, to extract the tabular data directly. However, these tools partially parsed the data, and the required format wasn’t achieved.

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

Here’s a snippet of the Python code used to achieve this:

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

            # Initialize index for character-by-character parsing
            index = 3
            
            # Extract network prefix (first field after "*")
            while index < len(parsed_line) and not parsed_line[index].isspace():
                network += parsed_line[index]
                index += 1
            
            # Skip whitespace after network prefix
            while index < len(parsed_line) and parsed_line[index].isspace():
                index += 1
            
            # Extract next hop address
            while index < len(parsed_line) and not parsed_line[index].isspace():
                next_hop += parsed_line[index]
                index += 1
            
            # Count whitespace to determine if metric exists
            white_space_count = 0
            while index < len(parsed_line) and parsed_line[index].isspace():
                white_space_count += 1
                index += 1
            
            # Handle metric field - set to None if large whitespace (missing metric)
            if white_space_count > 15:
                metric = None
            else:
                metric_string = ""
                # Extract metric value
                while index < len(parsed_line) and not parsed_line[index].isspace():
                    metric_string += parsed_line[index]
                    index += 1
                else:
                    metric = int(metric_string)  # Convert metric to integer
            
            # Skip whitespace after metric
            while index < len(parsed_line) and parsed_line[index].isspace():
                index += 1

            # Extract local preference value
            while index < len(parsed_line) and not parsed_line[index].isspace():
                locprf += parsed_line[index]
                index += 1
            
            # Skip whitespace after local preference
            while index < len(parsed_line) and parsed_line[index].isspace():
                index += 1

            # Extract weight value
            while index < len(parsed_line) and not parsed_line[index].isspace():
                weight += parsed_line[index]
                index += 1

            # Skip whitespace after weight
            while index < len(parsed_line) and parsed_line[index].isspace():
                index += 1

            # Extract AS path (remaining string)
            path = parsed_line[index:].strip() 

            # Prepare tuple of values for database insertion
            val = (network.strip(), next_hop.strip(), metric, locprf.strip(), weight.strip(), path.strip())

            # Execute SQL insert query with extracted values
            mycursor.execute(sql_query, val)
            count += mycursor.rowcount

# Commit all database insertions
mydb.commit()
print(count, "record inserted.")

# Clean up database connections
mycursor.close()
mydb.close()
```

""")




