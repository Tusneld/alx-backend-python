#!/usr/bin/python3
"""
Generator that streams rows from the SQL database one by one.
"""
import mysql.connector
seed = __import__('seed')


def stream_users():
    """
    Connects to the database and yields each row from the user_data table.
    Uses a generator to ensure memory efficiency.
    """
    connection = seed.connect_to_prodev()
    if connection:
        # dictionary=True allows access columns by name (e.g., row['name'])
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        # This loop yields one row at a time to the caller
        for row in cursor:
            yield row
            
        cursor.close()
        connection.close()