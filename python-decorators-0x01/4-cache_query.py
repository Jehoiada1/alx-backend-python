import time
import sqlite3
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator to handle opening and closing a database connection"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator to cache query results based on query string"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query in query_cache:
            print("Returning cached result for query.")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call — fetches from DB and caches result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call — returns from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users)
print(users_again)
