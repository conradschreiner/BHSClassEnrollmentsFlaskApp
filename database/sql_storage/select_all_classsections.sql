SELECT cs.classSectionID, cs.startDate AS "Class Start Date", cs.endDate AS "Class End Date",
       CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))AS "School Year",
       cs.period AS "Period", cs.classroom as "Classroom", c.name as "Course Name",
       CONCAT(t.fName, ' ', t.lName) AS "Teacher Name",
       t.isCurrentlyEmployed AS "Teacher Employment Status" -- including to better understand the NULLable foreign key
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;