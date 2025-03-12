SELECT s.studentID, CONCAT(CONCAT(s.fName, ' ', s.lName), ', ', gl.gradeName) as student_record
FROM `Students` s
INNER JOIN `GradeLevels` gl on s.gradeLevelID = gl.gradeLevelID;