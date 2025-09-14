def any_older_than(conn, age):
    # Counts the number of patients older than the given age
    if age < 0 or age > 100:
        print("Invalid age")
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM DBPNTHOL WHERE age > %s", age)
    result = cursor.fetchone()
    return result[0] > 0