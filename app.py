# We borrowed heavily from the provided Flask Starter app: https://github.com/osu-cs340-ecampus/flask-starter-app
# Citation for the following function: add_student()
# Date: 2/28/2025
# Source URL:  https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

import MySQLdb
import database.db_connector as db
import os
from flask import Flask, render_template, json, redirect, url_for
from flask_mysqldb import MySQL
from flask import request
from read_sql_file import read_sql_file
from contains_number import contains_number
import logging

app = Flask(__name__)

# configure app to our db
app.config['MYSQL_HOST'] = os.environ.get("340DBHOST") # replace with your database URL
app.config['MYSQL_USER'] = os.environ.get("340DBUSER") # replace with your database username
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW") # replace with your database password
app.config['MYSQL_DB'] = os.environ.get("340DB")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# set logger to debug mode for testing purposes messages
logging.basicConfig(level=logging.DEBUG)

mysql = MySQL(app)

# reusable functions for sql execution tasks
def run_select_query(query):
    """Executes and returns a mysql select query against the configured database."""
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def run_insert_query(query, values):
    """Executes and commits a mysql insert query against the configured database."""

    # initialize cursor
    cursor = mysql.connection.cursor()

    # execute given sql insert statement
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()

# exceptions
class NoNumberNameInput(Exception):
    """Flagged if a user tries to enter numerical values on an insert in an invalid scenario.
    source: https://www.geeksforgeeks.org/define-custom-exceptions-in-python/"""
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message, self.error_code)

    def __str__(self):
        return f"{self.message} (HTTPS Error Code: {self.error_code})"

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
    results_table = run_select_query(students_query)

    # pull available grade level names
    results_gl_dropdown = run_select_query(grade_levels_query)

    if results_table and results_gl_dropdown:
        # generate jinja template with data populated from database
        return render_template("students.j2", students=results_table, grade_levels=results_gl_dropdown)
    else:
        # display blank page with no data if the database has not been populated yet
        return render_template("students_no_data.html")

@app.route('/students/create', methods=["POST"])
def add_student():
    """Creates a new student record in the database."""
    # add student insert functionality
    if request.method == "POST":
        try:
            first_name = request.form["fName"]
            last_name = request.form["lName"]
            birthdate = request.form["birthdate"]
            grade_level = request.form["gradeLevel"]

            if contains_number(first_name) or contains_number(last_name):
                raise NoNumberNameInput("Numerical characters not allowed in student first name or last name.", 400)

            # store sql, data and prep cursor
            insert_sql = ("INSERT INTO `Students` (gradeLevelID, fName, lName, birthdate)"
                          "VALUES (%s, %s, %s, %s);")

            user_data = (grade_level, first_name, last_name, birthdate)

            # execute and commit query then close connection
            run_insert_query(insert_sql, user_data)

            return redirect("/students")

        except NoNumberNameInput as e:
            logging.error(f"Error adding student: {e}")
            return str(e), e.error_code

        except Exception as e:
            logging.error(f"Error adding student: {e}")
            return "There was an error adding the student.", 500


@app.route("/students/delete/<int:id>")
def delete_student(id):
    delete_sql = "DELETE FROM `Students` WHERE studentID = %s;"
    delete_cursor = mysql.connection.cursor()
    delete_cursor.execute(delete_sql, (id,))
    mysql.connection.commit()
    delete_cursor.close()
    return redirect("/students")


@app.route("/gradelevels", methods=["POST", "GET"])
def gradelevels():
    """Route CRUD methods to the GradeLevels Entity Page"""

    # load query from file and store as string variable
    grade_levels_query = read_sql_file(r"database/sql_storage/select_all_gradelevels.sql")

    # run query and generate jinja template
    results = run_select_query(grade_levels_query)

    return render_template("gradelevels.j2", gradelevels=results)

@app.route("/teachers", methods=["POST", "GET"])
def teachers():
    """Route CRUD methods to the Teachers Entity Page"""

    # load query from file and store as string variable
    teachers_query = read_sql_file(r"database/sql_storage/select_all_teachers.sql")

    # run query and generate jinja template
    results = run_select_query(teachers_query)

    return render_template("teachers.j2", teachers=results)

@app.route("/departments", methods=["POST", "GET"])
def departments():
    """Route CRUD methods to the Departments Entity Page"""

    # load query from file and store as string variable
    departments_query = read_sql_file(r"database/sql_storage/select_all_departments.sql")

    # run query and generate jinja template
    results = run_select_query(departments_query)

    return render_template("departments.j2", departments=results)

@app.route("/courses", methods=["POST", "GET"])
def courses():
    """Route CRUD methods to the Courses Entity Page"""

    # load query from file and store as string variable
    courses_query = read_sql_file(r"database/sql_storage/select_all_courses.sql")

    # run query and generate jinja template
    results = run_select_query(courses_query)

    return render_template("courses.j2", courses=results)

@app.route("/classsections", methods=["POST", "GET"])
def classsections():
    """Route CRUD methods to the ClassSections Entity Page"""

    # load query from file and store as string variable
    class_sections_query = read_sql_file(r"database/sql_storage/select_all_classsections.sql")

    # run query and generate jinja template
    results = run_select_query(class_sections_query)

    return render_template("classsections.j2", classsections=results)

@app.route("/enrollments", methods=["POST", "GET"])
def enrollments():
    """Route CRUD methods to the Enrollments Entity Page"""

    # load query from file and store as string variable
    enrollments_query = read_sql_file(r"database/sql_storage/select_all_enrollments.sql")

    # run query and generate jinja template
    results = run_select_query(enrollments_query)

    return render_template("enrollments.j2", enrollments=results)


# Listener
if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted

    port = int(os.environ.get('PORT', 3306))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
    #app.run(port=port)
