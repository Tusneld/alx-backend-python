import mysql.connector
import csv
import uuid

def connect_db():
    """Connects to the MySQL database server."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root", 
            password="tus" 
        )
    except mysql.connector.Error as err:
        return None

def create_database(connection):
    """Creates the database ALX_prodev."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    """Connects to the ALX_prodev database."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="tus", 
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        return None

def create_table(connection):
    """Creates the user_data table with an index on user_id."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10,2) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()

def insert_data(connection, file_path):
    """Inserts data from CSV and generates UUIDs for user_id."""
    cursor = connection.cursor()
    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Generate a unique UUID for each user
            user_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (user_id, row['name'], row['email'], row['age'])
            )
    connection.commit()
    cursor.close()