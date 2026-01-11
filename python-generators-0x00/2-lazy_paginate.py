#!/usr/bin/python3
"""
Lazy loading Paginated Data using generators
"""
import mysql.connector
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the database.
    
    Args:
        page_size (int): Number of rows to return.
        offset (int): Number of rows to skip.
    """
    connection = seed.connect_to_prodev()
    if connection:
        # Use dictionary=True so the rows are easy to read
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    return []


def lazy_pagination(page_size):
    """
    Generator that lazily loads each page from the database.
    Only fetches the next page when needed.
    """
    offset = 0
    while True:
        # Fetch the current page
        page = paginate_users(page_size, offset)
        
        # If the page is empty, we've reached the end of the data
        if not page:
            break
            
        # Yield the entire list of users in this page
        yield page
        
        # Increment the offset for the next call
        offset += page_size