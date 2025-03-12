SELECT cs.classSectionID, CONCAT(gl.gradeName, ' ', c.name, ' with ', IFNULL(CONCAT(t.fName, ' ', t.lName), 'no teacher yet assigned'),
    ' Classroom ', cs.classroom, ', Period ', cs.period,  ', ', CONCAT(YEAR(cs.startDate), '-', YEAR(cs.endDate))) as ClassSection
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
INNER JOIN `GradeLevels` gl on c.gradeLevelID = gl.gradeLevelID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;