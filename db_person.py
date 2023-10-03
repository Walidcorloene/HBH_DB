import sqlite3

# Connect to the SQLite database (creates a new database file if it doesn't exist)
connection = sqlite3.connect('person.db')

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Create the person table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS person (
    person_id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_source_value TEXT,
    gender_concept_id INTEGER,
    year_of_birth INTEGER
)
"""
cursor.execute(create_table_query)
print("Table 'person' created successfully.")

# Commit the changes and close the database connection
connection.commit()
connection.close()
print("Database connection closed.")
