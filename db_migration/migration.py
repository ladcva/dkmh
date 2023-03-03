# CAc mon hoc va Cac mon hoc cua hoc ky
# Template to migrate Data in Mysql using Python
import mysql.connector

# Connect to the source MySQL database
source_conn = mysql.connector.connect(
  host="source_host",
  user="source_user",
  password="source_password",
  database="source_database"
)

# Connect to the target MySQL database
target_conn = mysql.connector.connect(
  host="target_host",
  user="target_user",
  password="target_password",
  database="target_database"
)

# Create a cursor object for both databases
source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()

# Retrieve the data from the source database
source_cursor.execute("SELECT * FROM source_table")
data = source_cursor.fetchall()

# Loop through the data and insert it into the target database
for row in data:
  insert_query = "INSERT INTO target_table (column1, column2, column3) VALUES (%s, %s, %s)"
  values = (row[0], row[1], row[2])
  target_cursor.execute(insert_query, values)

# Commit the changes to the target database
target_conn.commit()

# Close the connections
source_conn.close()
target_conn.close()
