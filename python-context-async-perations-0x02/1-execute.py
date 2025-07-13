import sqlite3

class ExecuteQuery:
    """Context manager that executes a query with parameters and returns results"""
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.results = cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    print(results)
