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
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
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
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        )
    """)
    cursor.close()

def insert_data(connection, file_path):
    """Inserts data from the CSV into the database."""
    cursor = connection.cursor()
    try:
        with open(file_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Use existing user_id or generate a new one
                user_id = row.get('user_id', str(uuid.uuid4()))
                cursor.execute(
                    "INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (user_id, row['name'], row['email'], row['age'])
                )
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()