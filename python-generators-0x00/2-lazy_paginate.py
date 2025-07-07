from seed import connect_to_prodev

def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that lazily fetches paginated data one page at a time.
    """
    offset = 0
    while True:  # Single loop as required
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
