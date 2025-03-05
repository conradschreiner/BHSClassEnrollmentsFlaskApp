SELECT s.studentID, s.lName AS "Last Name", s.fName AS "First Name", s.birthdate AS "Birthdate",
       gl.gradeNumber AS "Grade Number", gl.gradeName AS "Grade Name"
FROM `Students` s
         INNER JOIN `GradeLevels` gl ON  s.gradeLevelID = gl.gradelevelID
ORDER BY s.studentID;