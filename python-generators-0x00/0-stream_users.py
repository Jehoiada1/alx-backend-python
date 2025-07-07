import sqlite3

def stream_users():
    """
    Generator that streams users from the user_data table
    in the user_data.db SQLite database one row at a time.
    """
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row  # So we get dict-like rows
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield dict(row)

    conn.close()
