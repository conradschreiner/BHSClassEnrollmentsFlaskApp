# from app import app
# import database.db_connector as db
# import os
# from flask import Flask, render_template, json, redirect
# from flask_mysqldb import MySQL
# from flask import request
#
#
#
#    # Grab students data so we send it to our template to display
#     if request.method == "GET":
#         # mySQL query to grab all the students in students
#         query = "SELECT students.id, fname, lname, bsg_planets.name AS homeworld, age FROM students LEFT JOIN bsg_planets ON homeworld = bsg_planets.id"
#         cur = mysql.connection.cursor()
#         cur.execute(query)
#         data = cur.fetchall()
#
#         # mySQL query to grab planet id/name data for our dropdown
#         query2 = "SELECT id, name FROM bsg_planets"
#         cur = mysql.connection.cursor()
#         cur.execute(query2)
#         homeworld_data = cur.fetchall()
#
#         # render edit_students page passing our query data and homeworld data to the edit_students template
#         return render_template("students.j2", data=data, homeworlds=homeworld_data)
#
#     # Separate out the request methods, in this case this is for a POST
#     # insert a person into the students entity
#     if request.method == "POST":
#         # fire off if user presses the Add Person button
#         if request.form.get("Add_Person"):
#             # grab user form inputs
#             fname = request.form["fname"]
#             lname = request.form["lname"]
#             homeworld = request.form["homeworld"]
#             age = request.form["age"]
#
#             # account for null age AND homeworld
#             if age == "" and homeworld == "0":
#                 # mySQL query to insert a new person into students with our form inputs
#                 query = "INSERT INTO students (fname, lname) VALUES (%s, %s)"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname))
#                 mysql.connection.commit()
#
#             # account for null homeworld
#             elif homeworld == "0":
#                 query = "INSERT INTO students (fname, lname, age) VALUES (%s, %s,%s)"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, age))
#                 mysql.connection.commit()
#
#             # account for null age
#             elif age == "":
#                 query = "INSERT INTO students (fname, lname, homeworld) VALUES (%s, %s,%s)"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, homeworld))
#                 mysql.connection.commit()
#
#             # no null inputs
#             else:
#                 query = "INSERT INTO students (fname, lname, homeworld, age) VALUES (%s, %s,%s,%s)"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, homeworld, age))
#                 mysql.connection.commit()
#
#             # redirect back to students page
#             return redirect("/students")
#
#
#
#
# # route for delete functionality, deleting a person from students,
# # we want to pass the 'id' value of that person on button click (see HTML) via the route
# @app.route("/delete_students/<int:id>")
# def delete_students(id):
#     # mySQL query to delete the person with our passed id
#     query = "DELETE FROM students WHERE id = '%s';"
#     cur = mysql.connection.cursor()
#     cur.execute(query, (id,))
#     mysql.connection.commit()
#
#     # redirect back to students page
#     return redirect("/students")
#
#
# # route for edit functionality, updating the attributes of a person in students
# # similar to our delete route, we want to the pass the 'id' value of that person on button click (see HTML) via the route
# @app.route("/edit_students/<int:id>", methods=["POST", "GET"])
# def edit_students(id):
#     if request.method == "GET":
#         # mySQL query to grab the info of the person with our passed id
#         query = f"SELECT * FROM students WHERE id = {id}"
#         cur = mysql.connection.cursor()
#         cur.execute(query)
#         data = cur.fetchall()
#
#         # mySQL query to grab planet id/name data for our dropdown
#         query2 = "SELECT id, name FROM bsg_planets"
#         cur = mysql.connection.cursor()
#         cur.execute(query2)
#         homeworld_data = cur.fetchall()
#
#         # render edit_students page passing our query data and homeworld data to the edit_students template
#         return render_template("edit_students.j2", data=data, homeworlds=homeworld_data)
#
#     # meat and potatoes of our update functionality
#     if request.method == "POST":
#         # fire off if user clicks the 'Edit Person' button
#         if request.form.get("Edit_Person"):
#             # grab user form inputs
#             id = request.form["personID"]
#             fname = request.form["fname"]
#             lname = request.form["lname"]
#             homeworld = request.form["homeworld"]
#             age = request.form["age"]
#
#             # account for null age AND homeworld
#             if (age == "" or age == "None") and homeworld == "0":
#                 # mySQL query to update the attributes of person with our passed id value
#                 query = "UPDATE students SET students.fname = %s, students.lname = %s, students.homeworld = NULL, students.age = NULL WHERE students.id = %s"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, id))
#                 mysql.connection.commit()
#
#             # account for null homeworld
#             elif homeworld == "0":
#                 query = "UPDATE students SET students.fname = %s, students.lname = %s, students.homeworld = NULL, students.age = %s WHERE students.id = %s"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, age, id))
#                 mysql.connection.commit()
#
#             # account for null age
#             elif age == "" or age == "None":
#                 query = "UPDATE students SET students.fname = %s, students.lname = %s, students.homeworld = %s, students.age = NULL WHERE students.id = %s"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, homeworld, id))
#                 mysql.connection.commit()
#
#             # no null inputs
#             else:
#                 query = "UPDATE students SET students.fname = %s, students.lname = %s, students.homeworld = %s, students.age = %s WHERE students.id = %s"
#                 cur = mysql.connection.cursor()
#                 cur.execute(query, (fname, lname, homeworld, age, id))
#                 mysql.connection.commit()
#
#             # redirect back to students page after we execute the update query
#             return redirect("/students")