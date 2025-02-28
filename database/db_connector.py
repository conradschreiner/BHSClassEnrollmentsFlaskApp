import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
import logging
import time

# Configure logging to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())


# Set the variables in our application with those environment variables
host = os.environ.get("340DBHOST") # replace with your database URL
user = os.environ.get("340DBUSER") # replace with your database username
passwd = os.environ.get("340DBPW") # replace with your database password
db = os.environ.get("340DB")

def connect_to_database(db_host = host, db_user = user, db_passwd = passwd, schema = db):
    '''
    connects to a database and returns a database objects
    '''
    db_connection = MySQLdb.connect(db_host,db_user,db_passwd,schema)
    return db_connection

def execute_query(db_connection = None, query = None, query_params = ()):
    '''
    executes a given SQL query on the given db connection and returns a Cursor object

    db_connection: a MySQLdb connection object created by connect_to_database()
    query: string containing SQL query

    returns: A Cursor object as specified at https://www.python.org/dev/peps/pep-0249/#cursor-objects.
    You need to run .fetchall() or .fetchone() on that object to actually acccess the results.

    '''

    if db_connection is None:
        logging.info("No connection to the database found! Have you called connect_to_database() first?")
        return None

    if query is None or len(query.strip()) == 0:
        logging.info("query is empty! Please pass a SQL query in query")
        return None

    logging.info(f"Executing {query} with {query_params}");
    # Create a cursor to execute query. Why? Because apparently they optimize execution by retaining a reference according to PEP0249
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)

    '''
    params = tuple()
    #create a tuple of paramters to send with the query
    for q in query_params:
        params = params + (q)
    '''
    #TODO: Sanitize the query before executing it!!!
    cursor.execute(query, query_params)
    # this will actually commit any changes to the database. without this no
    # changes will be committed!
    db_connection.commit()
    return cursor

if __name__ == '__main__':
    logging.info("Executing a sample query on the database using the credentials from db_credentials.py")
    db = connect_to_database()
    query = "SELECT * from students;"
    results = execute_query(db, query);
    logging.info(f"logging.infoing results of {query}")

    for r in results.fetchall():
        logging.info(r)