# We borrowed heavily from the provided Flask Starter app: https://github.com/osu-cs340-ecampus/flask-starter-app
# Citation for the following function: add_student()
# Date: 2/28/2025
# Source URL:  https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

import MySQLdb
import os
from flask import Flask, render_template, json, redirect, url_for
from flask_mysqldb import MySQL
from flask import request
from read_sql_file import read_sql_file
from contains_number import contains_number
import logging
from dotenv import load_dotenv, find_dotenv

# Load our environment variables from the .env file in the root of our project. - per starter-app 
load_dotenv(find_dotenv())

app = Flask(__name__)

# configure app to our db
app.config['MYSQL_HOST'] = os.environ.get("host")  # replace with your database URL
app.config['MYSQL_USER'] = os.environ.get("user")  # replace with your database username
app.config['MYSQL_PASSWORD'] = os.environ.get("passwd")  # replace with your database password
app.config['MYSQL_DB'] = os.environ.get("db")
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# set logger to debug mode for testing purposes messages
logging.basicConfig(level=logging.DEBUG)

mysql = MySQL(app)


# reusable functions for sql execution tasks
def run_select_query(query):
    """Executes and returns a mysql select query against the configured database.
    Inspired by db_connector.py on the https://github.com/osu-cs340-ecampus/flask-starter-app
    and referenced the MySQL python connector documentation heavily: https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html.
    However, the code itself was written by Conrad."""
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def run_select_params_query(query, values):
    """Executes and returns a mysql select query against the configured database.
    Inspired by db_connector.py on the https://github.com/osu-cs340-ecampus/flask-starter-app
    and referenced the MySQL python connector documentation heavily: https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html.
    However, the code itself was written by Conrad."""

    # initialize database cursor
    cursor = mysql.connection.cursor()

    # execute select query with the given parameters
    cursor.execute(query, values)
    return cursor.fetchall()


def run_change_query(query, values):
    """Executes and commits a mysql insert, update or delete query against the configured database.
    Inspired by db_connector.py on the https://github.com/osu-cs340-ecampus/flask-starter-app
    and referenced the MySQL python connector documentation heavily: https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html.
    However, the code itself was written and implemented by Conrad."""

    # initialize database cursor
    cursor = mysql.connection.cursor()

    # execute given sql insert, update or delete statement
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()


# exceptions
class NoNumberNameInput(Exception):
    """Flagged if a user tries to enter numerical values on an insert in an invalid scenario.
    source: https://www.geeksforgeeks.org/define-custom-exceptions-in-python/
    Also reference the official Python documentation her: https://docs.python.org/3/tutorial/errors.html
    Written and implemented by Conrad."""

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message, self.error_code)

    def __str__(self):
        return f"{self.message} (HTTPS Error Code: {self.error_code})"

# exceptions
class EmptyUpdateInput(Exception):
    """Flagged if a user tries to enter numerical values on an insert in an invalid scenario.
    source: https://www.geeksforgeeks.org/define-custom-exceptions-in-python/
    Also reference the official Python documentation her: https://docs.python.org/3/tutorial/errors.html
    Written and implemented by Conrad."""

    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message, self.error_code)

    def __str__(self):
        return f"{self.message} (HTTPS Error Code: {self.error_code})"

# Routes - Note that we did away with the strategy proposed on the starter app using the db_connector.py.
# The instructions seemed to jump back and forth between using it and not using it so we opted for implementing everything
# within app.py. Instead of executing queries with db_connetor.py like is provided in the starter app, we found that
# establishing the connection in the app itself, and then running the queries via run_select_query(), run_select_params_query()
# and run_change_query() was more effective and consistent.

@app.route('/')
def root():
    """Triggers the rendering of the homepage.
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing
    """
    # load schema diagram for homepage
    schema_image_file = url_for('static', filename='images/schema_webpage_layout.png')

    return render_template("index.j2", schema_image_file=schema_image_file)


@app.route("/students", methods=["GET", "POST"])
def students():
    """Route for Read functionality of Students Entity Page.
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing
    """

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
        return render_template("students_no_data.j2")


@app.route('/students/create', methods=["POST"])
def add_student():
    """Creates a new student record in the database.
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Conrad implemented the try and except blocks to handle errors more gracefully so that they don't crash the app.
    """

    # add student insert functionality
    if request.method == "POST":
        try:
            # get the input parameters provided by the user
            first_name = request.form["fName"]
            last_name = request.form["lName"]
            birthdate = request.form["birthdate"]
            grade_level = request.form["gradeLevel"]

            # prevent the user from using a numerical character in the first name or last name fields
            if contains_number(first_name) or contains_number(last_name):
                raise NoNumberNameInput("Numerical characters not allowed in student first name or last name.", 400)

            # store sql, data and prep cursor
            insert_sql = ("INSERT INTO `Students` (gradeLevelID, fName, lName, birthdate)"
                          "VALUES (%s, %s, %s, %s);")

            user_data = (grade_level, first_name, last_name, birthdate)

            # execute and commit query then close connection
            run_change_query(insert_sql, user_data)

            return redirect("/students")

        except NoNumberNameInput as e:
            logging.error(f"Error adding student: {e}")
            return str(e), e.error_code

        except Exception as e:
            logging.error(f"Error adding student: {e}")
            return "There was an error adding the student.", 500
@app.route("/students/update/<int:id>", methods=["POST"])
def update_student(id):
    if request.method == "POST":
        try: 
            
            first_name = request.form["fName_update"]
            last_name = request.form["lName_update"]
            birthdate = request.form["birthdate_update"]
            grade_level = request.form["gradeLevel_update"]

            update_sql = ("UPDATE `Students` SET lName = %s, fName = %s, birthdate = %s, gradeLevelID = %s WHERE studentID = %s;")
            run_change_query(update_sql, (last_name, first_name, birthdate, grade_level, id))
            return redirect("/students")
        except Exception as e: 
            logging.error(f"Error updating student: {e}")
            return "There was an error updating the student.", 500


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


@app.route("/gradelevels/create", methods=["POST"])
def add_grade_level():
    """Creates a new GradeLevel record in the database with the given user input
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Conrad implemented the try and except blocks to handle errors more gracefully so that they don't crash the app.
    """

    if request.method == "POST":
        try:
            # get the input parameters provided by the user
            grade_name = request.form["gradeName"]
            grade_num = request.form["gradeNum"]

            # prevent the user from using a numerical character in the grade level name
            if contains_number(grade_name):
                raise NoNumberNameInput("Numerical characters not allowed in GradeLevel name.", 400)

            insert_query = ("INSERT INTO `GradeLevels` (gradeName, gradeNumber)"
                            "VALUES (%s, %s);")

            insert_values = (grade_name, grade_num)

            run_change_query(insert_query, insert_values)

            return redirect("/gradelevels")

        except NoNumberNameInput as e:
            logging.error(f"Error adding grade level: {e}")
            return str(e), e.error_code

        except Exception as e:
            logging.error(f"Error adding grade level: {e}")
            return "There was an error adding the grade level.", 500


@app.route("/teachers", methods=["POST", "GET"])
def teachers():
    """Route CRUD methods to the Teachers Entity Page.
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    """

    # load query from file and store as string variable
    teachers_query = read_sql_file(r"database/sql_storage/select_all_teachers.sql")

    # run query and generate jinja template
    results = run_select_query(teachers_query)

    return render_template("teachers.j2", teachers=results)


@app.route("/teachers/create", methods=["POST"])
def add_teacher():
    """Creates a new teacher record in the database with the given user input.
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Conrad implemented the try and except blocks to handle errors more gracefully so that they don't crash the app.
    """
    if request.method == "POST":
        try:
            # get the input parameters provided by the user
            first_name = request.form["fName"]
            last_name = request.form["lName"]
            birthdate = request.form["birthdate"]

            # prevent the user from using a numerical character in the first name or last name fields
            if contains_number(first_name) or contains_number(last_name):
                raise NoNumberNameInput("Numerical characters not allowed in first name or last name.", 400)

            insert_query = ("INSERT INTO `Teachers` (fName, lName, birthdate)"
                            "VALUES (%s, %s, %s);")

            insert_values = (first_name, last_name, birthdate)

            # execute the query with values, commit and close connection
            run_change_query(insert_query, insert_values)

            return redirect("/teachers")

        except NoNumberNameInput as e:
            logging.error(f"Error adding teacher: {e}")
            return str(e), e.error_code

        except Exception as e:
            logging.error(f"Error adding teacher: {e}")
            return "There was an error adding the teacher.", 500

@app.route("/teachers/delete/<int:id>")
def delete_teacher(id):
    delete_sql = "DELETE FROM `Teachers` WHERE teacherID = %s;"
    delete_cursor = mysql.connection.cursor()
    delete_cursor.execute(delete_sql, (id,))
    mysql.connection.commit()
    delete_cursor.close()
    return redirect("/teachers")


@app.route("/departments", methods=["POST", "GET"])
def departments():
    """Route CRUD methods to the Departments Entity Page
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    """

    # load query from file and store as string variable
    departments_query = read_sql_file(r"database/sql_storage/select_all_departments.sql")

    # run query and generate jinja template
    results = run_select_query(departments_query)

    return render_template("departments.j2", departments=results)


@app.route("/departments/create", methods=["POST"])
def add_department():
    """Creates a new department record in the database with the given user input
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    """

    if request.method == "POST":
        try:
            subject_area = request.form["subjectArea"]

            insert_query = ("INSERT INTO `Departments` (subjectArea)"
                            "VALUES (%s);")

            # execute the query with values, commit and close connection
            run_change_query(insert_query, (subject_area,))

            return redirect("/departments")

        except Exception as e:
            logging.error(f"Error adding department: {e}")
            return "There was an error adding the department.", 500


@app.route("/courses", methods=["POST", "GET"])
def courses():
    """Route CRUD methods to the Courses Entity Page
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Drop-down functionality was adapted from @mlapresta's original repo that the flask starter app heavily borrows from, 
    specifically the people.html file where the dropdown for certificates is implemented: https://github.com/mlapresta/cs340_starter_app/blob/master/starter_website/templates/people.html
    The SQLs that populate the dropsoqns were written by Conrad. 
    """

    # load query from file and store as string variable
    courses_query = read_sql_file(r"database/sql_storage/select_all_courses.sql")
    departments_query = read_sql_file(r"database/sql_storage/select_department_subject_areas.sql")
    grade_levels_query = read_sql_file(r"database/sql_storage/select_gradelevel_names.sql")

    # run query and generate jinja template
    courses_table = run_select_query(courses_query)

    # pull available grade level names
    results_gl_dropdown = run_select_query(grade_levels_query)

    # pull available department subject areas
    results_dep_dropdown = run_select_query(departments_query)

    return render_template("courses.j2", courses=courses_table, grade_levels=results_gl_dropdown,
                           departments=results_dep_dropdown)


@app.route("/courses/create", methods=["POST"])
def add_course():
    """Creates a new course record in the database with the given user input"""
    if request.method == "POST":
        try:
            course_name = request.form["courseName"]
            department = request.form["department"]
            grade_level = request.form["gradeLevel"]

            insert_query = ("INSERT INTO `Courses` (gradeLevelID, name, departmentID)"
                            "VALUES (%s, %s, %s);")

            insert_values = (grade_level, course_name, department)

            # execute the query with values, commit and close connection
            run_change_query(insert_query, insert_values)

            return redirect("/courses")

        except Exception as e:
            logging.error(f"Error adding department: {e}")
            return "There was an error adding the department.", 500


@app.route("/classsections", methods=["POST", "GET"])
def classsections():
    """Route CRUD methods to the ClassSections Entity Page
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Drop-down functionality was adapted from @mlapresta's original repo that the flask starter app heavily borrows from, 
    specifically the people.html file where the dropdown for certificates is implemented: https://github.com/mlapresta/cs340_starter_app/blob/master/starter_website/templates/people.html
    The SQLs that populate the dropdowns were written by Conrad. 
    """

    # load query from file and store as string variable
    class_sections_query = read_sql_file(r"database/sql_storage/select_all_classsections.sql")
    teacher_names_query = read_sql_file(r"database/sql_storage/select_teacher_names.sql")
    course_names_query = read_sql_file(r"database/sql_storage/select_course_names.sql")

    # run query and generate jinja template
    class_sections_table = run_select_query(class_sections_query)
    teacher_dropdown = run_select_query(teacher_names_query)
    course_dropdown = run_select_query(course_names_query)

    return render_template("classsections.j2", classsections=class_sections_table, teachers=teacher_dropdown,
                           courses=course_dropdown)


@app.route("/classsections/create", methods=["POST"])
def add_classsection():
    """Creates a new classsection record in the database with the given user input
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Conrad implemented the try and except blocks to handle errors more gracefully so that they don't crash the app.
    """
    if request.method == "POST":
        try:
            course = request.form["course"]
            teacher = request.form["teacher"]
            period = request.form["period"]
            classroom = request.form["classroom"]
            start_date = request.form["startDate"]
            end_date = request.form["endDate"]

            # allow for teacher to be null
            if teacher == "0":
                insert_query = (
                    "INSERT INTO `ClassSections` (courseID, teacherID, startDate, endDate, period, classroom)"
                    "VALUES (%s, NULL, %s, %s, %s, %s);")

                insert_values = (course, start_date, end_date, period, classroom)

                # execute the query with values, commit and close connection
                run_change_query(insert_query, insert_values)

            # every scenario where the teacherID is NOT NULL
            else:
                insert_query = (
                    "INSERT INTO `ClassSections` (courseID, teacherID, startDate, endDate, period, classroom)"
                    "VALUES (%s, %s, %s, %s, %s, %s);")

                insert_values = (course, teacher, start_date, end_date, period, classroom)

                # execute the query with values, commit and close connection
                run_change_query(insert_query, insert_values)

            return redirect("/classsections")

        except Exception as e:
            logging.error(f"Error adding classsection: {e}")
            return "There was an error adding the classsection.", 500


@app.route('/classsections/update/<int:id>', methods=["GET", "POST"])
def update_classsection(id):
    """Prompts the user to edit the given classsection record on the row of the table.
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Conrad implemented the try and except blocks to handle errors more gracefully so that they don't crash the app.
    Drop-down functionality was adapted from @mlapresta's original repo that the flask starter app heavily borrows from, 
    specifically the people.html file where the dropdown for certificates is implemented: https://github.com/mlapresta/cs340_starter_app/blob/master/starter_website/templates/people.html
    The SQLs that populate the dropsoqns were written by Conrad. 
    """

    if request.method == "GET":

        # retrieve all data for the given classSectionID
        select_id_query = """SELECT cs.classSectionID, cs.startDate AS "Class Start Date", cs.endDate AS "Class End Date",
        CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate)) AS "School Year",
        cs.period AS "Period", cs.classroom AS "Classroom", c.name AS "Course Name",
        CONCAT(t.fName, ' ', t.lName) AS "Teacher Name"
        FROM `ClassSections` cs
        INNER JOIN `Courses` c ON cs.courseID = c.courseID
        LEFT JOIN `Teachers` t ON cs.teacherID = t.teacherID
        WHERE cs.classSectionID = %s;"""

        # store given classSectionID from the user's choice
        class_section_id = (id,)

        # run query and return the results of the given class section record data
        data = run_select_params_query(select_id_query, class_section_id)

        # drop down queries
        teacher_names_query = read_sql_file(r"database/sql_storage/select_teacher_names.sql")
        course_names_query = read_sql_file(r"database/sql_storage/select_course_names.sql")

        # run query and generate jinja template
        teacher_dropdown = run_select_query(teacher_names_query)
        course_dropdown = run_select_query(course_names_query)

        return render_template("update_classsection.j2", classsections=data, teachers=teacher_dropdown,
                               courses=course_dropdown)

    if request.method == "POST":
        try:
            teacher = request.form["teacher"]
            period = request.form["period"]
            classroom = request.form["classroom"]
            start_date = request.form["startDate"]
            end_date = request.form["endDate"]

            # store request responses as dictionary for filtering
            field_dict = {"period": period, "classroom": classroom, "startDate": start_date, "endDate": end_date}

            # filter dictionary to remove any pairs that contain an empty value
            field_dict_filtered = {k: v for k, v in field_dict.items() if v != ""}

            # dynamically create SET list from filtered dictionary
            update_set_list = [f"{k} = %s" for k in field_dict_filtered.keys()]

            if not update_set_list:
                raise EmptyUpdateInput("You did not select any fields to update which results in a MySQL 1064 error - please try again.", 400)

            # update to new teacher
            if teacher != "0" and teacher != "n":
                update_set_list.append("teacherID = %s")
                update_values = list(field_dict_filtered.values()) + [teacher, id]

            # set teacher to NULL - "NULLable" relationship
            elif teacher == "n":
                update_set_list.append("teacherID = NULL")
                # exclude teacher field from update so that current one is maintained
                update_values = list(field_dict_filtered.values()) + [id]

            # maintain teacher
            else:
                update_values = list(field_dict_filtered.values()) + [id]

            update_query = f"UPDATE `ClassSections` SET {', '.join(update_set_list)} WHERE classSectionID = %s;"
            run_change_query(update_query, update_values)

            return redirect("/classsections")

        except EmptyUpdateInput as e:
            logging.error(f"Error updating classsection due to no fields being selected: {e}")
            return str(e), e.error_code

        except Exception as e:
            logging.error(f"Error updating classsection: {e}")
            return "There was an error updating the classsection.", 500

@app.route("/enrollments", methods=["POST", "GET"])
def enrollments():
    """Route CRUD methods to the Enrollments Entity Page
    Followed the template guidelines set by the starter app https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-4---templates.
    Also referenced the Flask "Quickstart" documentation heavily: https://flask.palletsprojects.com/en/stable/quickstart/#routing.
    Drop-down functionality was adapted from @mlapresta's original repo that the flask starter app heavily borrows from, 
    specifically the people.html file where the dropdown for certificates is implemented: https://github.com/mlapresta/cs340_starter_app/blob/master/starter_website/templates/people.html
    The SQLs that populate the dropsdowns were written by Conrad. 
    """

    # load queries from files and store as string variables
    enrollments_query = read_sql_file(r"database/sql_storage/select_all_enrollments.sql")
    student_names_query = read_sql_file(r"database/sql_storage/select_student_names.sql")
    class_sections_query = read_sql_file(r"database/sql_storage/class_section_dropdown.sql")

    # run queries and generate jinja templates
    enrollments_table = run_select_query(enrollments_query)

    # this dynamic drop down contains student name and grade level name
    student_dropdown = run_select_query(student_names_query)

    # this dynamic dropdown contains all relevant class section fields so the user can make an accurate choice
    class_section_dropdown = run_select_query(class_sections_query)

    return render_template("enrollments.j2", enrollments=enrollments_table, students=student_dropdown,
                           class_sections=class_section_dropdown)


@app.route("/enrollments/create", methods=["POST"])
def add_enrollment():
    """Creates a new enrollment record in the database with the given user input.

    Conrad implemented the try and except blocks to handle errors more gracefully so that they don't crash the app.
    """

    if request.method == "POST":
        try:
            # get user input
            student = request.form["student"]
            class_section = request.form["class_section"]

            insert_query = ("INSERT INTO `Enrollments` (studentID, classSectionID, enrolledDate)"
                            "VALUES (%s, %s, CURRENT_DATE);")

            insert_values = (student, class_section)

            run_change_query(insert_query, insert_values)

            return redirect("/enrollments")

        except Exception as e:
            logging.error(f"Error adding enrollment: {e}")
            return "There was an error adding the enrollment.", 500


# Listener
if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted

    port = int(os.environ.get('PORT', 3322))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
    #app.run(port=port)
