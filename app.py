import database.db_connector as db
import os
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from read_sql_file import read_sql_file
import logging
import time

# store current run date for logging files
run_date_log = time.strftime('%Y-%m-%d-%H:%M')

log_filename = fr'program_logs\run_log_app_{run_date_log}.txt'

# Configure logging to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

mysql = MySQL(app)

db_connection = db.connect_to_database()


# Routes
@app.route('/')
def root():
    """Triggers the rendering of the homepage."""
    return render_template("index.j2")


@app.route("/students.j2", methods=["POST", "GET"])
def students():
    """Route CRUD methods to the Students Entity Page"""

    students_query = read_sql_file(r"database/sql_storage/select_all_students.sql")

    cursor = db.execute_query(db_connection=db_connection, query=students_query)
    results = cursor.fetchall()
    logging.info(f"Results: {results}")
    return render_template("students.j2", students=results)

# Listener
if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted
    # app.run(port=3306, debug=True)
    port = int(os.environ.get('PORT', 3306))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port)
