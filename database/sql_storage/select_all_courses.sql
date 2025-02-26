SELECT c.courseID, c.name as "Course Name", c.isCurrentlyOffered AS "Currently Offered Course",
       gl.gradeName AS "Grade Level Name", gl.gradeNumber AS "Grade Level Number",
       d.subjectArea AS "Department Subject Area"
FROM `Courses` c
INNER JOIN `Departments` d ON  c.departmentID = d.departmentID
INNER JOIN `GradeLevels` gl ON c.gradeLevelID = gl.gradeLevelID
ORDER BY c.courseID;