-- -------------------------------------------------------------------------------------------------------------
-- Citation
-- Unless otherwise noted, all SQL queries were written by our team using the MySQL documentation for reference.
-- https://dev.mysql.com/doc/refman/9.2/en/sql-statements.html
-- For the use of CONCAT in SELECT statements, this website was used for reference: https://www.mysqltutorial.org/mysql-string-functions/mysql-concat/
-- MySQL documentation for IFNULL() used in the ClassSections table SELECT query https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull
-- -------------------------------------------------------------------------------------------------------------

-- ---------------------------------------------------
-- Queries used to grab all data FROM each given table
-- ---------------------------------------------------

-- gradeLevels webpage table Query
SELECT gl.gradeLevelID, gl.gradeName as "Grade Name", gl.gradeNumber as "Grade Number"
FROM `GradeLevels` gl
ORDER BY gl.gradeLevelID;

-- Students webpage table query that we plan to use for student page to show grade level foreign key join
SELECT s.studentID, s.lName AS "Last Name", s.fName AS "First Name", s.birthdate AS "Birthdate",
       gl.gradeNumber AS "Grade Number", gl.gradeName AS "Grade Name"
FROM `Students` s
         INNER JOIN `GradeLevels` gl ON  s.gradeLevelID = gl.gradelevelID
ORDER BY s.studentID; -- going to go with order by PK for now on every table query

-- Teachers webpage table Query 
SELECT t.teacherID, t.fName AS "First Name", t.lName AS "Last Name", t.birthdate as "Birthdate"
FROM `Teachers` t
ORDER BY t.teacherID;

-- Departments webpage table Query
SELECT d.departmentID, d.subjectArea AS "Department Subject Area"
FROM `Departments` d
ORDER BY d.departmentID;

-- Courses webpage table Query - includes foreign key joins on departments and gradelevels for user visibility
SELECT c.courseID, c.name as "Course Name", c.gradeLevelID,
       gl.gradeName AS "Grade Level Name", gl.gradeNumber AS "Grade Level Number", d.departmentID,
       d.subjectArea AS "Department Subject Area"
FROM `Courses` c
INNER JOIN `Departments` d ON  c.departmentID = d.departmentID
INNER JOIN `GradeLevels` gl ON c.gradeLevelID = gl.gradeLevelID
ORDER BY c.courseID;


-- classSections webpage table query - includes foreign key joins on Courses and Teachers for uses visibility
SELECT cs.classSectionID, cs.startDate AS "Class Start Date", cs.endDate AS "Class End Date",
       CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
       cs.period AS "Period", cs.classroom as "Classroom", c.name as "Course Name", gl.gradeName as "Course Grade Name",
       CONCAT(t.fName, ' ', t.lName) AS "Teacher Name" -- including to better understand the NULLable foreign key
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
INNER JOIN `GradeLevels` gl on c.gradeLevelID = gl.gradeLevelID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;

-- Enrollments table Query - includes foreign key joins plus addition joins from ClassSection to show the details of the given ClassSection record (needed for accurately inserting enrollments)
SELECT e.enrollmentID, e.enrolledDate as "Date Student Enrolled",
       CONCAT(s.fName, ' ', s.lName) AS "Enrolled Student Name",
       cs.period AS "Period", cs.classroom AS "Classroom",
       CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
       c.name AS "Course Name", gl.gradeName as "Course Grade Name",
       CONCAT(t.fName, ' ', t.lName) AS "ClassSection's Teacher Name"
FROM `Enrollments` e
INNER JOIN `Students` s ON e.studentID = s.studentID
INNER JOIN `ClassSections` cs ON e.classSectionID = cs.classSectionID
INNER JOIN `Courses` c ON c.courseID = cs.courseID
INNER JOIN `GradeLevels` gl ON c.gradeLevelID = gl.gradeLevelID
LEFT JOIN `Teachers` t ON cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY e.enrollmentID;

-- --------------------------------------------------------------------------------------------------------
-- insert statements - user will have dropdown options for each foreign key (using a relevant attribute)
-- --------------------------------------------------------------------------------------------------------
-- gradelevels - designed to not be manipulated, but included due to project requirements
INSERT INTO `GradeLevels` (gradeName, gradeNumber)
VALUES (%s, %s);

-- students
INSERT INTO `Students` (gradeLevelID, fName, lName, birthdate)
VALUES (%s, %s, %s, %s);

-- select gradeNames for gradeLevelID FK dropdown - only the gradeName is displayed. The ID is used behind the scenes for the <options> values.
SELECT gradeLevelID, gradeName -- This also allows for the FK to be used directly in the INSERT instead of a subquery
    FROM `GradeLevels`;

-- Teachers
INSERT INTO `Teachers` (fName, lName, birthdate)
VALUES (%s, %s, %s);

-- department
INSERT INTO `Departments` (subjectArea)
                            VALUES (%s);

-- Courses
INSERT INTO `Courses` (gradeLevelID, name, departmentID)
VALUES (%s, %s, %s);

-- select gradeNames for gradeLevelID FK dropdown - only the gradeName is displayed. The ID is used behind the scenes for the <options> values.
SELECT gradeLevelID, gradeName -- This also allows for the FK to be used directly in the INSERT instead of a subquery
    FROM `GradeLevels`;

-- select subjectAreas for departmentID FK dropdown
SELECT subjectArea
FROM Departments;

-- classSections
INSERT INTO `ClassSections` (courseID, teacherID, startDate, endDate, period, classroom)
VALUES (%s, NULL, %s, %s, %s, %s);


-- select course names for dropdown on classSectionID FK
SELECT name -- :courseName --options
FROM `Courses`;

-- select full teacher names for the class section teacherID FK
SELECT teacherID, CONCAT(fName, ' ', lName) as "fullName" FROM `Teachers`;

-- enrollments
INSERT INTO `Enrollments` (studentID, classSectionID, enrolledDate)
VALUES (%s, %s, CURRENT_DATE);

-- select full student name for dropdown on studentID FK - also include student grade level
SELECT s.studentID, CONCAT(CONCAT(s.fName, ' ', s.lName), ', ', gl.gradeName) as student_record
FROM `Students` s
INNER JOIN `GradeLevels` gl on s.gradeLevelID = gl.gradeLevelID;

-- select relevant ClassSection data to be displayed for dropdown on classSectionID FK
SELECT cs.classSectionID, CONCAT(gl.gradeName, ' ', c.name, ' with ', IFNULL(CONCAT(t.fName, ' ', t.lName), 'no teacher yet assigned'),
    ' Classroom ', cs.classroom, ', Period ', cs.period,  ', ', CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))) as ClassSection
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
INNER JOIN `GradeLevels` gl on c.gradeLevelID = gl.gradeLevelID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;


-- -----------------
-- Update Statements
-- -----------------

-- UPDATE ClassSections
-- The Python function in app.py update_classsection(id) dynamically creates the update statements based on user input.
-- This dynamic enables update statements that only include the fields that the user entered in the SET clause, which results in more efficient queries that 
-- are not executing redundant updates that set a field to the same value it was already listed as.
-- the foreign key teacherID on ClassSections can be set to NULL here via a dropdown option, to achieve the requirement of removing a relationship aka "NULLable"
-- {', '.join(update_set_list)} fills the SET clause with the fields the USER wants to update, such as teacherID = NULL, period = 1, etc.

UPDATE `ClassSections` SET {', '.join(update_set_list)} WHERE classSectionID = %s;

-- select classSectionID from the row where the user clicks the button
SELECT cs.classSectionID, cs.startDate AS "Class Start Date", cs.endDate AS "Class End Date",
        CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate)) AS "School Year",
        cs.period AS "Period", cs.classroom AS "Classroom", c.name AS "Course Name",
        CONCAT(t.fName, ' ', t.lName) AS "Teacher Name"
        FROM `ClassSections` cs
        INNER JOIN `Courses` c ON cs.courseID = c.courseID
        LEFT JOIN `Teachers` t ON cs.teacherID = t.teacherID
        WHERE cs.classSectionID = %s;


-- UPDATE Students
UPDATE `Students` SET lName = %s, fName = %s, birthdate = %s, gradeLevelID = %s WHERE studentID = %s;

-- -----------------
-- Delete Statements
-- -----------------

-- DELETE Students
-- removes a chosen student FROM the database - note that delete cascade is implemented ON enrollments
DELETE FROM `Students` WHERE studentID = %s;

-- DELETE Teachers
DELETE FROM `Teachers` WHERE teacherID = %s;