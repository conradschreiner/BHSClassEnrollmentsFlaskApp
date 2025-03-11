SELECT cs.classSectionID, cs.startDate AS "Class Start Date", cs.endDate AS "Class End Date",
       CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
       cs.period AS "Period", cs.classroom as "Classroom", c.name as "Course Name", gl.gradeName as "Course Grade Name",
       CONCAT(t.fName, ' ', t.lName) AS "Teacher Name" -- including to better understand the NULLable foreign key
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
INNER JOIN `GradeLevels` gl on c.gradeLevelID = gl.gradeLevelID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;