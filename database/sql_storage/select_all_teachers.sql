SELECT t.teacherID, t.fName AS "First Name", t.lName AS "Last Name", t.isCurrentlyEmployed AS "Employment Status"
FROM `Teachers` t
ORDER BY t.teacherID;