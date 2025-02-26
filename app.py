import database.db_connector as db
import os
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from read_sql_file import read_sql_file

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

    # load query from file and store as string variable
    students_query = read_sql_file(r"database/sql_storage/select_all_students.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=students_query)
    results = cursor.fetchall()
    return render_template("students.j2", students=results)

@app.route("/gradelevels.j2", methods=["POST", "GET"])
def gradelevels():
    """Route CRUD methods to the GradeLevel Entity Page"""

    # load query from file and store as string variable
    gradelevels_query = read_sql_file(r"database/sql_storage/select_all_gradelevels.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=gradelevels_query)
    results = cursor.fetchall()
    return render_template("gradelevels.j2", gradelevels=results)


# Listener
if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted
    # app.run(port=3306, debug=True)
    port = int(os.environ.get('PORT', 3306))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port)
