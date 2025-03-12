SELECT s.studentID, CONCAT('Full Name - ', CONCAT(s.fName, ' ', s.lName), ' | Grade Level - ', gl.gradeName) as student_record
FROM `Students` s
INNER JOIN `GradeLevels` gl on s.gradeLevelID = gl.gradeLevelID;