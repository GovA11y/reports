

def execute_sql_from_file(conn, filename, domain):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sql_file = fd.read()
    fd.close()

    # format SQL command
    formatted_sql_file = sql_file % domain

    # Execute SQL commands
    cursor = conn.cursor()
    cursor.execute(formatted_sql_file)

    # Fetch result
    result = cursor.fetchall()

    # Commit the transaction
    conn.commit()

    return result