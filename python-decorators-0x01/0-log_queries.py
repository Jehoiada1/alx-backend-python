import sqlite3
import functools
import time  # Use time instead of datetime

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('example.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime())
        print(f"{timestamp} Executing: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@with_db_connection
@log_queries
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Example usage
user = get_user_by_id(user_id=1)
print(user)

