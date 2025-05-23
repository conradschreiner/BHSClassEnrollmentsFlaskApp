-- note that we had issues with the ClassSectionsID being a foreign key on two tables, per the recommendation here of making unique foreign key "names" for each table, 
-- we were able to resolve SQL error 1826 based on advice from this stackoverflow post: https://stackoverflow.com/questions/51589929/mysql-forward-engineering-error-1826
-- In previous versions there were commented out index statements from the MySQL forward engineering. Those have been deleted since indexing is beyond the scope of this course.
-- Citation:
-- CREATE TABLEs were first generated using forward engineering, and have since been manually refactored by our team.
-- INTERTS were written by the team with reference to the Module 3 Exploration of SQL resources, and the MySQL official documentaton: https://dev.mysql.com/doc/heatwave/en/mys-hw-insert-select.html

-- MySQL Workbench Forward Engineering
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Professor recommended constraint for autocommit and data checks
SET AUTOCOMMIT = 0;
SET unique_checks=0;
SET foreign_key_checks=0;
-- 
-- -----------------------------------------------------
-- Schema cs340_schrecon
-- -----------------------------------------------------
-- CREATE SCHEMA IF NOT EXISTS `cs340_schrecon` DEFAULT CHARACTER SET utf8 ; -- use this if creating database locally
USE `cs340_schrecon` ; -- use this if running on flip or class server

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`GradeLevels`
-- ----------------------------------------------------
DROP TABLE IF EXISTS `cs340_schrecon`.`GradeLevels` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`GradeLevels` (
  `gradeLevelID` INT NOT NULL AUTO_INCREMENT,
  `gradeName` VARCHAR(45) NOT NULL,
  `gradeNumber` INT(2) NOT NULL,
  PRIMARY KEY (`gradeLevelID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`Students`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cs340_schrecon`.`Students` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`Students` (
  `studentID` INT NOT NULL AUTO_INCREMENT,
  `gradeLevelID` INT NOT NULL,
  `fName` VARCHAR(45) NOT NULL,
  `lName` VARCHAR(45) NOT NULL,
  `birthdate` DATE NOT NULL,
  PRIMARY KEY (`studentID`),
  CONSTRAINT `idGradeLevel`
    FOREIGN KEY (`gradeLevelID`)
    REFERENCES `cs340_schrecon`.`GradeLevels` (`gradeLevelID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`Teachers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cs340_schrecon`.`Teachers` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`Teachers` (
  `teacherID` INT NOT NULL AUTO_INCREMENT,
  `fName` VARCHAR(45) NOT NULL,
  `lName` VARCHAR(45) NOT NULL,
  `birthdate` DATE NOT NULL, -- functions like a boolean True or False
  PRIMARY KEY (`teacherID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`Departments`
-- -----------------------------------------------------

DROP TABLE IF EXISTS `cs340_schrecon`.`Departments` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`Departments` (
  `departmentID` INT NOT NULL AUTO_INCREMENT,
  `subjectArea` VARCHAR(45) NOT NULL UNIQUE,
  PRIMARY KEY (`departmentID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`Courses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cs340_schrecon`.`Courses` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`Courses` (
  `courseID` INT NOT NULL AUTO_INCREMENT,
  `gradeLevelID` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `departmentID` INT NOT NULL,
  PRIMARY KEY (`courseID`),
  CONSTRAINT `gradeLevelID`
    FOREIGN KEY (`gradeLevelID`)
    REFERENCES `cs340_schrecon`.`GradeLevels` (`gradeLevelID`)
		ON UPDATE CASCADE,
    CONSTRAINT `departmentID`
    FOREIGN KEY (`departmentID`)
    REFERENCES `cs340_schrecon`.`Departments` (`departmentID`)
		ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`ClassSections`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cs340_schrecon`.`ClassSections` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`ClassSections` (
  `classSectionID` INT NOT NULL AUTO_INCREMENT,
  `courseID` INT NOT NULL,
  `teacherID` INT,
  `startDate` DATE NOT NULL,
  `endDate` DATE NOT NULL,
  `period` INT(2) NOT NULL,
  `classroom` INT(3) NOT NULL,
  PRIMARY KEY (`classSectionID`),
  CONSTRAINT `courseID`
    FOREIGN KEY (`courseID`)
    REFERENCES `cs340_schrecon`.`Courses` (`courseID`)
		ON UPDATE CASCADE,
  CONSTRAINT `teacherID`
    FOREIGN KEY (`teacherID`)
    REFERENCES `cs340_schrecon`.`Teachers` (`teacherID`)
    ON DELETE SET NULL ) -- if a teacher record is deleted, then set to null
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cs340_schrecon`.`Enrollments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `cs340_schrecon`.`Enrollments` ;

CREATE TABLE IF NOT EXISTS `cs340_schrecon`.`Enrollments` (
  `enrollmentID` INT NOT NULL AUTO_INCREMENT,
  `studentID` INT NOT NULL,
  `classSectionID` INT NOT NULL,
  `enrolledDate` DATE NOT NULL,
  PRIMARY KEY (`enrollmentID`),
  CONSTRAINT `idStudent`
    FOREIGN KEY (`studentID`)
    REFERENCES `cs340_schrecon`.`Students` (`studentID`)
    ON DELETE CASCADE, -- this is in reference to the "DELETable" record - ensuring the DELETE is normalized through the DB
  CONSTRAINT `classSectionID`
    FOREIGN KEY (`classSectionID`)
    REFERENCES `cs340_schrecon`.`ClassSections` (`classSectionID`)
    ON UPDATE CASCADE -- this is for the "NULLable" M:M relationship - ensuring the UPDATE is normalized through the DB
)
ENGINE = InnoDB;

-- GradeLevels
INSERT INTO `cs340_schrecon`.`GradeLevels`
(`gradeName`, `gradeNumber`)
VALUES
('Freshman', 9), ('Sophomore', 10), ('Junior', 11), ('Senior', 12);

-- teachers
INSERT INTO `cs340_schrecon`.`Teachers`
(`fName`, `lName`, `birthdate`)
VALUES ('Kate', 'Jones', '1980-03-19'), ('Brandon', 'Lynn', '1990-11-24'),
    ('Dave', 'Kim', '1975-07-02'), ('Ruth', 'Rosenberg', '1980-12-31'),
    ('Sandra', 'Springfield', '1981-11-12'), 
		('Valentina', 'Murphy', '1985-05-01'),
		('Tom', 'Rossi', '1968-10-15'),
		('Juanita', 'Gomez', '1998-06-30') ; -- teacher that has just been hired but has not been assigned any class sections yet


-- Students
INSERT INTO `cs340_schrecon`.`Students`
(`gradeLevelID`, `fName`, `lName`, `birthdate`) 
VALUES ((SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeNumber` = 9), 'Molly', 'Brown', '2009-11-08'), 
((SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeNumber` = 10), 'Adam', 'Armstrong', '2009-05-20'), 
((SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where  `gradeNumber` = 11), 'Priyanka', 'Patel', '2007-07-11'),
((SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeNumber` = 11), 'Rahul', 'Patel', '2007-07-11');

-- Students additional sample data
INSERT INTO `cs340_schrecon`.`Students` (`gradeLevelID`, `fName`, `lName`, `birthdate`) 
VALUES ((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 9), 'Paul', 'Paulson', '2009-11-08'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 9), 'John', 'Johnson', '2009-11-17'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 12), 'Robert', 'Robertson', '2009-08-07'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 12), 'Fredrick', 'Fredrickson', '2012-01-10'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 9), 'Olaf', 'Olafson', '2009-08-07'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 12), 'Howard', 'Howardson', '2007-10-09'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 10), 'Erik', 'Erikson', '2009-06-04'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 10), 'Sarah', 'Smith', '2009-03-11'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 10), 'Hideo', 'Kojima', '2009-06-25'),
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 11), 'Paul', 'Atreides', '2008-07-12'), -- note: this student has only had one class section enrollment - a class section can have only one student in it
((SELECT `gradeLevelID` FROM `cs340_schrecon`.`GradeLevels` WHERE `gradeNumber` = 12), 'Ximena', 'Cuaron', '2007-07-12');

-- Departments
INSERT INTO `cs340_schrecon`.`Departments`
(`subjectArea`)
VALUES ('English'), ('History'), ('Math'), ('Science'), ('Electives'), ('Foreign Languages');

-- Courses
INSERT INTO `cs340_schrecon`.`Courses`
(`gradeLevelID`, `name`, `departmentID`)
VALUES 
(	-- Freshman level English Course
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Freshman'), 
	'English', 
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'English')
), 
(	-- Freshman Spanish, no ClassSections yet
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Freshman'), 
	'Spanish', 
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'Foreign Languages')
),
(	-- Drivers Ed Elective
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Sophomore'), 
	"Driver's Ed", 
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'Electives')
),
(	-- Sophomore level Geometry
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Sophomore'), 
	'Geometry', 
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'Math')
),
(	-- Anatomy and Physiology, no ClassSections yet
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Junior'),
	'Anatomy and Physiology',
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'Science')
),
( 	-- Junior level US History
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Junior'),
	'US History',
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'History')
	
),
(	-- Senior level AP Calc
	(SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Senior'), 
	'AP Calculus', 
	(SELECT `departmentID` from `cs340_schrecon`.`Departments` where `subjectArea` = 'Math')
);

-- ClassSections
INSERT INTO `cs340_schrecon`.`ClassSections`
(`courseID`, `teacherID`, `startDate`, `endDate`, `period`, `classroom`)
VALUES ( -- Freshman English with Kate Jones, Period 9, Classroom 77
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'English'), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Kate' and `lName` = 'Jones'), 
	'2024-09-01', 
	'2025-06-01',  
	9, 
	77
),
(	-- Senior AP Calc taught by Brandon Lynn, Period 2, Classroom 13
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus'), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn'), 
	'2024-09-01', 
	'2025-06-01',  
	2, 
	13
),
(	-- Senior AP Calc course taught by Ruth Rosenberg, Period 9, Classroom 25
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus'), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Ruth' and `lName` = 'Rosenberg'), 
	'2024-09-01', 
	'2025-06-01',  
	9, 
	25
),
(	-- Senior AP Calc course taught by Ruth Rosenberg, Period 3, Classroom 25
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus'), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Ruth' and `lName` = 'Rosenberg'), 
	'2024-09-01', 
	'2025-06-01',  
	3, 
	25
),
(	-- Sophomore Geometry course taught by Brandon Lynn, Period 8, Classroom 74
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Geometry'),
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn'), 
	'2024-09-01', 
	'2025-06-01',  
	8, 
	74
	
),
(	-- Sophomore Driver's Ed course taught by Dave Kim, Period 5, Classroom 120
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = "Driver's Ed"), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Dave' and `lName` = 'Kim'),
	'2023-09-01', 
	'2024-06-01', 
	5, 
	120
),
(	-- Junior US History course taught by Sandra Springfield, Period 2, Classroom 20
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'US History'), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Sandra' and `lName` = 'Springfield'),
	'2024-09-01', 
	'2025-06-01', 
	2, 
	20
),
(	-- Freshman Spanish course taught by Valentina Murphy, Period 7, Classroom 14
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Spanish' and `gradeLevelID` = (SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Freshman')), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Valentina' and `lName` = 'Murphy'),
	'2024-09-01', 
	'2025-06-01', 
	7, 
	14
),
(	-- Junior Anatomy and Physiology course taught by Tom Rossi, Period 3, Classroom 18
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Anatomy and Physiology'), 
	(SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Tom' and `lName` = 'Rossi'),
	'2024-09-01', 
	'2025-06-01', 
	3, 
	18
),
( -- Freshman English with no Teacher selected yet, Period 10, Classroom 50
	(SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'English'),
	NULL,
	'2024-09-01',
	'2025-06-01',
	10,
	50
)
;

-- Enrollments
INSERT INTO `cs340_schrecon`.`Enrollments`
(`studentID`, `classSectionID`,`enrolledDate`) 
VALUES
 ( -- Molly Brown in Freshman English class section taught by Kate Jones
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Molly' and `lName` = 'Brown'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
	`courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'English')
	and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Kate' and `lName` = 'Jones')), 
	'2024-08-10'
), 
( -- Priyanka Patel in US History class section taught by Sandra Springfield
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Priyanka' and `lName` = 'Patel'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'US History')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Sandra' and `lName` = 'Springfield')),
    '2024-08-01'
),
(
	-- Priyanka Patel in Drivers ED class section taught by Dave Kim
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Priyanka' and `lName` = 'Patel'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = "Driver's Ed")
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Dave' and `lName` = 'Kim')), 
	'2023-08-10'
),
(	-- Rahul Patel in Drivers Ed class section taugth by Date Kim
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Rahul' and `lName` = 'Patel'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = "Driver's Ed")
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Dave' and `lName` = 'Kim')), 
	'2023-08-10'
),
(	-- Paul Paulson in English class section taught by Kate Jones
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Paul' and `lName` = 'Paulson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
	`courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'English') 
	and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Kate' and `lName` = 'Jones')), 
	'2024-08-10'
),
(	-- John Johnson in English class section taught by Kate Jones
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'John' and `lName` = 'Johnson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
	`courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'English') 
	and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Kate' and `lName` = 'Jones')), 
	'2024-08-10'
), 
(	-- Robert Robertson in AP Calc class section taught by Ruth Rosenberg
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Robert' and `lName` = 'Robertson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Ruth' and `lName` = 'Rosenberg')
    and `period` = 3), -- for teachers who teach more than one period, the classSection sbuquery needs to include period and/or classroom
	'2024-08-10'
), 
(	-- Howard Howardson in AP Calc class section taught by Ruth Rosenberg
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Howard' and `lName` = 'Howardson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Ruth' and `lName` = 'Rosenberg')
    and `period` = 9), 
	'2024-08-10'
),
(	-- Olaf Olafson in Freshman English class section taught by Kate Jones
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Olaf' and `lName` = 'Olafson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
	`courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'English') 
	and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Kate' and `lName` = 'Jones')), 
	'2024-08-10'
), 
(	-- Fredrick Fredrickson in AP Calc class section taught by Ruth Rosenberg
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Fredrick' and `lName` = 'Fredrickson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Ruth' and `lName` = 'Rosenberg')
    and `period` = 9), 
	'2024-08-10'
),
(-- Adam Armstrong in Geometry class section taught by Brandon Lynn
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Adam' and `lName` = 'Armstrong'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Geometry')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn')), 
	'2024-08-10'
),
(-- Erik Erikson in Geometry class section taught by Brandon Lynn
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Erik' and `lName` = 'Erikson'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Geometry')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn')), 
	'2024-08-10'
),
( -- Sarah Smith in Geometry class section taught by Brandon Lynn
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Sarah' and `lName` = 'Smith'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Geometry')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn')), 
	'2024-08-10'
),
( -- Hideo Kojima in Geometry class section taught by Brandon Lynn
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Hideo' and `lName` = 'Kojima'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Geometry')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn')), 
	'2024-08-10'
),
( -- Paul Atreides in US History class section taught by Sandra Springfield
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Paul' and `lName` = 'Atreides'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'US History')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Sandra' and `lName` = 'Springfield')), 
	'2024-08-10'
),
( -- Ximena Cuaron in AP Calc class section taught by Brandon Lynn
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Ximena' and `lName` = 'Cuaron'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'AP Calculus')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Brandon' and `lName` = 'Lynn')), 
	'2024-08-10'
),
(-- Rahul Patel in Anatomy and Physiology class section taught by Tom Rossi
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Rahul' and `lName` = 'Patel'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Anatomy and Physiology')
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Tom' and `lName` = 'Rossi')), 
	'2024-08-10'
),
(-- Molly Brown in Spanish class section taught by Valentina Murphy
	(SELECT `studentID` from `cs340_schrecon`.`Students` where `fName` = 'Molly' and `lName` = 'Brown'),
	(SELECT `classSectionID` from `cs340_schrecon`.`ClassSections` where 
    `courseID` = (SELECT `courseID` from `cs340_schrecon`.`Courses` where `name` = 'Spanish' and `gradeLevelID` = (SELECT `gradeLevelID` from `cs340_schrecon`.`GradeLevels` where `gradeName` = 'Freshman'))
    and `teacherID` = (SELECT `teacherID` from `cs340_schrecon`.`Teachers` where `fName` = 'Valentina' and `lName` = 'Murphy')), 
	'2024-08-10'
)
;

-- my sql forward engineering constraint
SET SQL_MODE=@OLD_SQL_MODE;

-- undo Professor recommended constraint for autocommit and data checks
SET unique_checks=1;
SET foreign_key_checks=1;

-- finalize database dump/import
COMMIT;