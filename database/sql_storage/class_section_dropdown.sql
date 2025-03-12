SELECT cs.classSectionID, CONCAT('Course Name - ', c.name, ' | Grade Level - ', gl.gradeName,
                        ' | Teacher - ', IFNULL(CONCAT(t.fName, ' ', t.lName), 'Not yet assigned'),
                        ' | Period - ', cs.period, ' | Classroom - ', cs.classroom,  ' | Start Date - ', cs.startDate,
                        ' | End Date - ', cs.endDate) as ClassSection
FROM `ClassSections` cs
INNER JOIN `Courses` c on cs.courseID = c.courseID
INNER JOIN `GradeLevels` gl on c.gradeLevelID = gl.gradeLevelID
LEFT JOIN `Teachers` t on cs.teacherID = t.teacherID -- to account for NULL and/or "NULLed" Teachers
ORDER BY cs.classSectionID;