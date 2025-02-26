-- ---------------------------------------------------
-- Queries used to grab all data FROM each given table
-- ---------------------------------------------------

-- gradeLevels webpage table Query
SELECT gl.gradeLevelID, gl.gradeName as "Grade Name", gl.gradeNumber as "Grade Number"
FROM `GradeLevels` gl
ORDER BY gl.gradeLevelID;

-- Students webpage table query that we plan to use for student page to show grade level foreign key join
SELECT s.studentID, s.lName AS "Last Name", s.fName AS "First Name", s.birthdate AS "Birthdate", s.gradeLevelID, gl.gradeName AS "Grade Name"
FROM `Students` s
         INNER JOIN `GradeLevels` gl ON  s.gradeLevelID = gl.gradelevelID
ORDER BY s.studentID; -- going to go with order by PK for now on every table query

-- Teachers webpage table Query 
SELECT t.teacherID, t.fName AS "First Name", t.lName AS "Last Name"
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
       cs.period AS "Period", cs.classroom as "Classroom", c.courseID, c.name as "Course Name",
       t.teacherID, CONCAT(t.fName, ' ', t.lName) AS "Teacher Name"
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;



-- Enrollments table Query - includes foreign key joins plus addition joins from ClassSection to show the details of the given ClassSection record (needed for accurately inserting enrollments)
SELECT e.enrollmentID, e.enrolledDate as "Date Student Enrolled", e.studentID,
       CONCAT(s.fName, ' ', s.lName) AS "Enrolled Student Name",
       cs.classSectionID, cs.period AS "Period", cs.classroom AS "Classroom",
       CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
       c.name AS "Course Name", CONCAT(t.fName, ' ', t.lName) AS "ClassSection's Teacher Name"
FROM `Enrollments` e
INNER JOIN `Students` s ON e.studentID = s.studentID
INNER JOIN `ClassSections` cs ON e.classSectionID = cs.classSectionID
INNER JOIN `Courses` c ON c.courseID = cs.courseID
LEFT JOIN `Teachers` t ON cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY e.enrollmentID;

-- --------------------------------------------------------------------------------------------------------
-- insert statements - user will have dropdown options for each foreign key (using a relevant attribute)
-- --------------------------------------------------------------------------------------------------------
-- gradelevels - designed to not be manipulated, but included due to project requirements
INSERT INTO `Gradelevels` (gradeName, gradeNumber)
VALUES (
        :gradeNameInput, -- basic text input field
        :gradeNumberInput -- basic text input field
       );

-- students
INSERT INTO `Students`
(`gradeLevelID`, `fName`, `lName`, `birthdate`) -- for gradeLevel, user will only be able to from available GradeLevel.gradeName(s)
VALUES (
        (SELECT `gradeLevelID` FROM `GradeLevels` WHERE `gradeNumber` = :gradeNumber),
        :fNameInput,  -- text box iput
        :lNameInput, -- text box input
        :birthdateInput -- date select input
);

-- use for grade dropdown on insert
SELECT gradeName -- :gradeNumber options
    FROM gradelevels;

-- Teachers
INSERT INTO `Teachers` (fName, lName, birthdate)
VALUES (
        :fNameInput, -- text box input
        :lNameInput, -- text box input
        :birthdateInput -- date select input
       );

-- department
INSERT INTO `Departments` (subjectArea)
VALUES (
        :subjectAreaInput -- basic text input field
       );

-- Courses
INSERT INTO `Courses` (gradeLevelID, name, departmentID)
VALUES (
        (SELECT gradeLevelID FROM `GradeLevels` WHERE gradeNumber = :gradeNumber),
        :nameInput, -- text box input
        (SELECT departmentID FROM `Departments` WHERE subjectArea = :subjectArea)
       );

-- select gradeNames for gradeLevelID FK dropdown
SELECT gradeName -- :gradeNumber options
    FROM gradelevels;

-- select subjectAreas for departmentID FK dropdown
SELECT subjectArea -- :subjectArea options
FROM Departments;

-- classSections
INSERT INTO `ClassSections` (courseID, teacherID, startDate, endDate, period, classroom)
VALUES (
        (SELECT courseID FROM `Courses` WHERE name = :courseName),
        (SELECT teacherID FROM `Teachers` WHERE CONCAT(fName, ' ', lName) = :teacherFullName), -- derived FROM subquery ON  backend - dynamic dropdown list for user
        :startDateInput, -- date input field
        :endDateInput, -- date input field
        :periodInput, -- static drop down list of available periods
        :classroomInput -- static drop down of available classrooms
       );

-- select course names for dropdown on classSectionID FK
SELECT name -- :courseName --options
FROM `Courses`;

-- select full teacher names for the class section teacherID FK
SELECT CONCAT(fName, ' ', lName) -- :teacherFullName option
FROM `Teachers`;

-- enrollments
INSERT INTO `Enrollments` (studentID, classSectionID, enrolledDate)
VALUES ( -- subquery to find studentID based on dropdown selection - student full name
        (SELECT studentID FROM `Students` WHERE CONCAT(fName, ' ', lName) = :studentFullName),
        ( -- subquery to find classSectionID based on dropdown selections - teacher full name and course name
        SELECT classSectionID
        FROM `ClassSections`
        WHERE teacherID = (SELECT teacherID FROM `Teachers` WHERE CONCAT(fName, ' ', lName) = :teacherFullName)
        AND courseID = (SELECT courseID FROM `Courses` WHERE name = :courseName)                                                ),
        CURRENT_DATE
       );

-- select full student name for dropdown on studentID FK
SELECT CONCAT(fName, ' ', lName) -- :studentFullName
FROM `Students`;

-- select ClassSection.teacherID for dropdown on classSectionID FK
SELECT CONCAT(fName, ' ', lName) -- :teacherFullName option
FROM `Teachers`;

-- select ClassSection.courseID for dropdown on classSectionID FK
SELECT name -- :courseName --options
FROM `Courses`;


-- -----------------
-- Update Statements
-- -----------------

-- the foreign key teacherID ON classSections to NULL, to achieve the requirement of removing a relationship
UPDATE `ClassSections`
SET
    courseID = (SELECT courseID FROM `Courses` WHERE name = :courseName),
    teacherID = (SELECT teacherID FROM `Teachers` WHERE CONCAT(fName, ' ', lName) = :teacherFullName),
    startDate = :startDate,
    endDate = :endDate,
    period = :period,
    classroom = :classroom
WHERE
    classSectionID = :classSectionIDInput -- this will be applied via a row by row "edit" button on the table - ideally a popup window for dropdowns
;

-- select full teacher names for the class section teacherID FK - ideally can store these in a list and add NULL as option
SELECT CONCAT(fName, ' ', lName) -- :teacherFullName option
FROM `Teachers`;

-- select ClassSection.courseID for dropdown on classSectionID FK
SELECT name -- :courseName --options
FROM `Courses`;

-- -----------------
-- Delete Statements
-- -----------------

-- removes a chosen student FROM the database - note that delete cascade is implemented ON enrollments
DELETE
FROM `Students`
WHERE
    studentID = :studentID -- this will be applied via a row by row "remove" button on the table
;

-- ------------------------------------------------------------------------------------------------------------------------------------
-- Data Queries to show relationships and a more comprehensive view of the database - not sure if these are going to be implemented yet
-- ------------------------------------------------------------------------------------------------------------------------------------

-- Registrar Query - an overall view of all enrollments of students in class sections - registrar.html
-- SELECT c.name AS "Course Name", concat(t.fName, ' ', t.lName) AS "Teacher Name",
--          cs.classroom AS "Classroom", cs.period AS "Period",
--          CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
--          s.fName AS "Student First Name", s.lName AS "Student Last Name"
--   FROM `ClassSections` cs
--            INNER JOIN `Teachers` t ON  cs.teacherID = t.teacherID
--            INNER JOIN `Enrollments` e ON  cs.classSectionID = e.classSectionID
--            INNER JOIN `Students` s ON  e.studentID = s.studentID
--            INNER JOIN `Courses` c ON  cs.courseID = c.courseID
--   ORDER BY cs.endDate desc, c.courseID, cs.classSectionID, s.studentID
-- ;
-- 
-- -- Course Catalog Query - an overall view of all Courses and their class sections - courseCatalog.html
-- SELECT d.subjectArea AS "Department Subject Area", c.name  AS "Course Name",
--        gl.gradeName AS "Grade Name", gl.gradeNumber AS "Grade Number"
-- FROM `Courses` c
--          INNER JOIN `Departments` d ON  c.departmentID = d.departmentID
--          INNER JOIN `Gradelevels` gl ON  c.gradeLevelID = gl.gradeLevelID
-- ORDER BY gl.gradeNumber, d.departmentID, c.courseID
-- ;



