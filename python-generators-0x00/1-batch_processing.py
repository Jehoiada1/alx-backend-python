import sqlite3

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
    """
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")
    batch = []

    for row in cursor:
        batch.append(dict(row))
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    conn.close()


def batch_processing(batch_size):
    """
    Processes each batch and prints users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
