import sqlite3

def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data table.
    """
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    conn.close()

def compute_average_age():
    """
    Uses the stream_user_ages generator to compute average age
    without loading all ages into memory.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 1
        total_age += age
        count += 1

    average = total_age / count if count else 0
    print(f"Average age of users: {average:.2f}")

if __name__ == "__main__":
    compute_average_age()
