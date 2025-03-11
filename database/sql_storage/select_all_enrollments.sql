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