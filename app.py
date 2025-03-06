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

app = Flask(__name__)

# configure app to our db
app.config['MYSQL_HOST'] = os.environ.get("340DBHOST")  # replace with your database URL
app.config['MYSQL_USER'] = os.environ.get("340DBUSER")  # replace with your database username
app.config['MYSQL_PASSWORD'] = os.environ.get("340DBPW")  # replace with your database password
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


def run_select_params_query(query, values):
    """Executes and returns a mysql select query against the configured database."""
    cursor = mysql.connection.cursor()
    cursor.execute(query, values)
    return cursor.fetchall()


def run_change_query(query, values):
    """Executes and commits a mysql insert, update or delete query against the configured database."""

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
            run_change_query(insert_sql, user_data)

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


@app.route("/gradelevels/create", methods=["POST"])
def add_grade_level():
    """Creates a new GradeLevel record in the database with the given user input"""
    if request.method == "POST":
        try:
            grade_name = request.form["gradeName"]
            grade_num = request.form["gradeNum"]

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
    """Route CRUD methods to the Teachers Entity Page"""

    # load query from file and store as string variable
    teachers_query = read_sql_file(r"database/sql_storage/select_all_teachers.sql")

    # run query and generate jinja template
    results = run_select_query(teachers_query)

    return render_template("teachers.j2", teachers=results)


@app.route("/teachers/create", methods=["POST"])
def add_teacher():
    """Creates a new teacher record in the database with the given user input"""
    if request.method == "POST":
        try:
            first_name = request.form["fName"]
            last_name = request.form["lName"]
            birthdate = request.form["birthdate"]

            if contains_number(first_name) or contains_number(last_name):
                raise NoNumberNameInput("Numerical characters not allowed in first name or last name.", 400)

            insert_query = ("INSERT INTO `Teachers` (fName, lName, birthdate)"
                            "VALUES (%s, %s, %s);")

            insert_values = (first_name, last_name, birthdate)

            run_change_query(insert_query, insert_values)

            return redirect("/teachers")

        except NoNumberNameInput as e:
            logging.error(f"Error adding teacher: {e}")
            return str(e), e.error_code

        except Exception as e:
            logging.error(f"Error adding teacher: {e}")
            return "There was an error adding the teacher.", 500


@app.route("/departments", methods=["POST", "GET"])
def departments():
    """Route CRUD methods to the Departments Entity Page"""

    # load query from file and store as string variable
    departments_query = read_sql_file(r"database/sql_storage/select_all_departments.sql")

    # run query and generate jinja template
    results = run_select_query(departments_query)

    return render_template("departments.j2", departments=results)


@app.route("/departments/create", methods=["POST"])
def add_department():
    """Creates a new department record in the database with the given user input"""

    if request.method == "POST":
        try:
            subject_area = request.form["subjectArea"]

            insert_query = ("INSERT INTO `Departments` (subjectArea)"
                            "VALUES (%s);")

            run_change_query(insert_query, (subject_area,))

            return redirect("/departments")

        except Exception as e:
            logging.error(f"Error adding department: {e}")
            return "There was an error adding the department.", 500


@app.route("/courses", methods=["POST", "GET"])
def courses():
    """Route CRUD methods to the Courses Entity Page"""

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

            run_change_query(insert_query, insert_values)

            return redirect("/courses")

        except Exception as e:
            logging.error(f"Error adding department: {e}")
            return "There was an error adding the department.", 500


@app.route("/classsections", methods=["POST", "GET"])
def classsections():
    """Route CRUD methods to the ClassSections Entity Page"""

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
    """Creates a new classsection record in the database with the given user input"""
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

                run_change_query(insert_query, insert_values)
            else:
                insert_query = (
                    "INSERT INTO `ClassSections` (courseID, teacherID, startDate, endDate, period, classroom)"
                    "VALUES (%s, %s, %s, %s, %s, %s);")

                insert_values = (course, teacher, start_date, end_date, period, classroom)

                run_change_query(insert_query, insert_values)

            return redirect("/classsections")

        except Exception as e:
            logging.error(f"Error adding classsection: {e}")
            return "There was an error adding the classsection.", 500


@app.route('/classsections/update/<int:id>', methods=["GET", "POST"])
def update_classsection(id):
    """Prompts the user to edit the given classsection record on the row of the table."""
    if request.method == "GET":
        # retrieve all data for the given classSectionID
        select_id_query = """SELECT cs.classSectionID, cs.startDate AS "Class Start Date", cs.endDate AS "Class End Date",
        CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
        cs.period AS "Period", cs.classroom as "Classroom", c.name as "Course Name",
        CONCAT(t.fName, ' ', t.lName) AS "Teacher Name" -- including to better understand the NULLable foreign key
        FROM `ClassSections` cs
        INNER JOIN `Courses` c on cs.courseID = c.courseID
        LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID
        WHERE cs.classSectionID = %s;"""
        class_section_id = (id,)
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
            course = request.form["course"]
            teacher = request.form["teacher"]
            period = request.form["period"]
            classroom = request.form["classroom"]
            start_date = request.form["startDate"]
            end_date = request.form["endDate"]

            # dynamically build the update statement by storing the SET fields and values in lists based on request.form responses
            update_fields = []
            update_values = []

            # if course response value is not "0" then include, if is 0 then exclude
            if course != "0":
                update_fields.append("courseID = %s")
                update_values.append(course)

            # if teacher response is not "0" then include request, if it is "0" then set to NULL
            if teacher != "0":
                update_fields.append("teacherID = %s")
                update_values.append(teacher)
            else:
                update_fields.append("teacherID = NULL")

            # if startDate response value is not "0" then include, if is 0 then exclude
            if start_date != "0":
                update_fields.append("startDate = %s")
                update_values.append(start_date)

            # if endDate response value is not "0" then include, if is 0 then exclude
            if end_date != "0":
                update_fields.append("endDate = %s")
                update_values.append(end_date)

            # if period response value is not "0" then include, if is 0 then exclude
            if period != "0":
                update_fields.append("period = %s")
                update_values.append(period)

            # if classroom response value is not "0" then include, if is 0 then exclude
            if classroom != "0":
                update_fields.append("classroom = %s")
                update_values.append(classroom)

            update_values.append(id)

            update_query = f"UPDATE `ClassSections` SET {', '.join(update_fields)} WHERE classSectionID = %s;"

            run_change_query(update_query, update_values)
            return redirect("/classsections")

        except Exception as e:
            logging.error(f"Error updating classsection: {e}")
            return "There was an error updating the classsection.", 500

@app.route("/enrollments", methods=["POST", "GET"])
def enrollments():
    """Route CRUD methods to the Enrollments Entity Page"""

    # load query from file and store as string variable
    enrollments_query = read_sql_file(r"database/sql_storage/select_all_enrollments.sql")
    student_names_query = read_sql_file(r"database/sql_storage/select_student_names.sql")
    course_names_query = read_sql_file(r"database/sql_storage/select_course_names.sql")
    teacher_names_query = read_sql_file(r"database/sql_storage/select_teacher_names.sql")

    # run query and generate jinja template
    enrollments_table = run_select_query(enrollments_query)
    student_dropdown = run_select_query(student_names_query)
    course_dropdown = run_select_query(course_names_query)
    teacher_dropdown = run_select_query(teacher_names_query)

    return render_template("enrollments.j2", enrollments=enrollments_table, students=student_dropdown,
                           courses=course_dropdown, teachers=teacher_dropdown)


@app.route("/enrollments/create", methods=["POST"])
def add_enrollment():
    """Creates a new enrollment record in the database with the given user input"""
    if request.method == "POST":
        try:
            student = request.form["student"]
            course = request.form["course"]
            teacher = request.form["teacher"]
            period = request.form["period"]
            classroom = request.form["classroom"]

            insert_query = ("INSERT INTO `Enrollments` (studentID, classSectionID, enrolledDate)"
                            "VALUES (%s, "
                            "(SELECT classSectionID FROM `ClassSections` WHERE teacherID = %s AND courseID = %s AND period = %s AND classroom = %s),"
                            "CURRENT_DATE);")

            insert_values = (student, teacher, course, period, classroom)

            run_change_query(insert_query, insert_values)

            return redirect("/enrollments")

        except Exception as e:
            logging.error(f"Error adding enrollment: {e}")
            return "There was an error adding the enrollment.", 500


# Listener
if __name__ == "__main__":
    #Start the app on port 3000, it will be different once hosted

    port = int(os.environ.get('PORT', 3306))
    #                                 ^^^^
    #              You can replace this number with any valid port

    app.run(port=port, debug=True)
    #app.run(port=port)
