#!/usr/bin/python3
"""
Batch processing Large Data using generators
"""
import mysql.connector
seed = __import__('seed')


def stream_users_in_batches(batch_size):
    """
    Fetches rows from the user_data table in batches.
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            # fetchmany retrieves the next set of rows of a query result
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield rows
            
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter and print users over the age of 25.
    """
    # Outer loop for batches
    for batch in stream_users_in_batches(batch_size):
        # Inner loop for users within the batch
        for user in batch:
            if user['age'] > 25:
                print(user)