# Writen by Conrad so that SQL queries could be stored in seperate files for organization, and then stored as string variables
# when needed. It is used in all of the pages READ functions, as well as on all of the dropdowns that Conrad worked on.
# Utlized Python's built-in open() function and referenced it using the official Python documentation: https://docs.python.org/3/library/functions.html#open.

def read_sql_file(sql_file):
    """Reads a sql file and returns it as a string.
    Utilized Python's built-in open() function and referenced it using the official Python documentation: 
    https://docs.python.org/3/library/functions.html#open.
    """

    with open(sql_file) as f:
        return f.read()