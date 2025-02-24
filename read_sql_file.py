def read_sql_file(sql_file):
    """Reads a sql file and returns it as a string"""

    with open(sql_file) as f:
        return f.read()