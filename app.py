import MySQLdb

import database.db_connector as db
import os
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from read_sql_file import read_sql_file
import logging

app = Flask(__name__)

# set logger to debug mode for testing purposes messages
logging.basicConfig(level=logging.DEBUG)


mysql = MySQL(app)

db_connection = db.connect_to_database()


# Routes
@app.route('/')
def root():
    """Triggers the rendering of the homepage."""
    return render_template("index.j2")


@app.route("/students", methods=["GET", "POST"])
def students():
    """Route for Read functionality of Students Entity Page"""

    # load read queries from file and store as string variable
    students_query = read_sql_file(r"database/sql_storage/select_all_students.sql")
    grade_levels_query = read_sql_file(r"database/sql_storage/select_gradelevel_names.sql")

    # run table query and fetch results
    cursor_table = db.execute_query(db_connection=db_connection, query=students_query)
    results_table = cursor_table.fetchall()

    # pull available grade level names
    cursor_grade_levels = db.execute_query(db_connection=db_connection, query=grade_levels_query)
    results_grade_levels = cursor_grade_levels.fetchall()

    # generate jinja template
    return render_template("students.j2", students=results_table, grade_levels=results_grade_levels)

@app.route('/students/create', methods=["POST"])
def add_student():
    """Creates a new student record in the database."""
    # add student insert functionality
    if request.method == "POST" and request.form.get("add_student"):
        first_name = request.form["fName"]
        last_name = request.form["lName"]
        birtdate = request.form["birthdate"]
        gradelevel = request.form["gradelevel"]

        # store sql, data and prep cursor - source: https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        insert_sql = ("INSERT INTO `Students` (gradeLevelID, fName, lName, birthdate)"
                      "VALUES (%s, %s, %s, %s);")

        user_data = (gradelevel, first_name, last_name, birtdate)
        cursor_insert = mysql.connection.cursor()

        # execute query
        cursor_insert.execute(insert_sql, user_data)

        # commit the insert
        mysql.connection.commit()

        return redirect("/students")

@app.route("/gradelevels", methods=["POST", "GET"])
def gradelevels():
    """Route CRUD methods to the GradeLevels Entity Page"""

    # load query from file and store as string variable
    gradelevels_query = read_sql_file(r"database/sql_storage/select_all_gradelevels.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=gradelevels_query)
    results = cursor.fetchall()
    return render_template("gradelevels.j2", gradelevels=results)

@app.route("/teachers", methods=["POST", "GET"])
def teachers():
    """Route CRUD methods to the Teachers Entity Page"""

    # load query from file and store as string variable
    teachers_query = read_sql_file(r"database/sql_storage/select_all_teachers.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=teachers_query)
    results = cursor.fetchall()
    return render_template("teachers.j2", teachers=results)

@app.route("/departments", methods=["POST", "GET"])
def departments():
    """Route CRUD methods to the Departments Entity Page"""

    # load query from file and store as string variable
    departments_query = read_sql_file(r"database/sql_storage/select_all_departments.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=departments_query)
    results = cursor.fetchall()
    return render_template("departments.j2", departments=results)

@app.route("/courses", methods=["POST", "GET"])
def courses():
    """Route CRUD methods to the Courses Entity Page"""

    # load query from file and store as string variable
    courses_query = read_sql_file(r"database/sql_storage/select_all_courses.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=courses_query)
    results = cursor.fetchall()
    return render_template("courses.j2", courses=results)

@app.route("/classsections", methods=["POST", "GET"])
def classsections():
    """Route CRUD methods to the ClassSections Entity Page"""

    # load query from file and store as string variable
    classsections_query = read_sql_file(r"database/sql_storage/select_all_classsections.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=classsections_query)
    results = cursor.fetchall()
    return render_template("classsections.j2", classsections=results)

@app.route("/enrollments", methods=["POST", "GET"])
def enrollments():
    """Route CRUD methods to the Enrollments Entity Page"""

    # load query from file and store as string variable
    enrollments_query = read_sql_file(r"database/sql_storage/select_all_enrollments.sql")

    # run query and generate jinja template
    cursor = db.execute_query(db_connection=db_connection, query=enrollments_query)
    results = cursor.fetchall()
    return render_template("enrollments.j2", enrollments=results)


# Listener
if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted

    port = int(os.environ.get('PORT', 3306))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
    #app.run(port=port)
