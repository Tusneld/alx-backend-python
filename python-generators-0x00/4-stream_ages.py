#!/usr/bin/python3
"""
Memory-efficient aggregation using generators
"""
import mysql.connector
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields only the age column from user_data.
    """
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield float(row['age'])
        cursor.close()
        connection.close()


def calculate_average_age():
    """
    Calculates the average age without loading the entire dataset into memory.
    """
    total_age = 0
    count = 0
    
    # Using the generator allows us to process 1 row at a time
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average}")


if __name__ == "__main__":
    calculate_average_age()