--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT X.*,
       GPA
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
    SELECT *
    FROM (VALUES ('Wade', 'Luly', 'Biology', 'Health Sciences'),
('Kieran', 'McGuire', 'Biology', NULL),
('Tess', 'Prendergast', 'Biology', 'Elementary Education'),
('Landen', 'Conner', 'Biochemistry/Molecular Biology', NULL),
('Daxon', 'Graham', 'Biology', NULL),
('Mariah', 'Moran', 'Anthrozoology', 'Biochemistry/Molecular Biology'),
('Katherine', 'Bold', 'Biochemistry/Molecular Biology', NULL),
('Mila', 'Duncan', 'Biochemistry/Molecular Biology', NULL),
('Macie', 'Frans', 'Biochemistry/Molecular Biology', NULL),
('Rachel', 'Kaiser', 'Biochemistry/Molecular Biology', NULL),
('Carson', 'Lewis', 'Biochemistry/Molecular Biology', NULL),
('Adisyn', 'O''Connor', 'Biochemistry/Molecular Biology', NULL),
('Vicente', 'Ortega', 'Biochemistry/Molecular Biology', NULL),
('Zackery', 'Prokopyschyn', 'Biochemistry/Molecular Biology', NULL),
('Mederise', 'Tooke', 'Biochemistry/Molecular Biology', NULL),
('Corinne', 'Anderko', 'Biology', NULL),
('Emma', 'Boharski', 'Biology', NULL),
('Clara', 'Carpenter', 'Biology', NULL),
('Marrin', 'Chapman', 'Biology', 'Catholic Studies'),
('Laura', 'DeBowes', 'Biology', NULL),
('Michael', 'Deguzman', 'Biology', NULL),
('Josie', 'Gale', 'Biology', NULL),
('Terra', 'Hurt', 'Biology', NULL),
('Chloe', 'Jones', 'Biology', NULL),
('Edouard', 'Karleskind', 'Biology', NULL),
('Maximilien', 'Karleskind', 'Biology', NULL),
('Serena', 'Keil-Hoye', 'Biology', NULL),
('June', 'Lepage', 'Biology', 'Hispanic Studies and Languages'),
('Trey', 'Melton', 'Biology', NULL),
('Michal', 'Mojzis', 'Biology', NULL),
('Megan', 'Olsen', 'Biology', 'Hispanic Studies and Languages'),
('Hunter', 'Peck', 'Biology', NULL),
('Nathan', 'Stalder', 'Biology', NULL),
('Kenna', 'Thomas', 'Biology', NULL),
('Caleb', 'Smith', 'Environmental Science', 'Biology'),
('Bryce', 'Hall', 'Biology', NULL))
    AS DF(First_Name, Last_Name, Major1, Major2)
--(End 1)------------------------------------------------------------------------------------------------------------
     ) AS X
LEFT JOIN (
SELECT STUDENT_FIRST_NAME,
       STUDENT_LAST_NAME,
       STP_EVAL_COMBINED_GPA AS GPA
FROM STUDENT_ACAD_PROGRAMS_VIEW
WHERE STP_START_DATE <= GETDATE()
AND (STP_END_DATE IS NULL OR STP_END_DATE > DATEADD(YEAR, -1, GETDATE()))
AND STP_CURRENT_STATUS IN ('Active', 'Graduated')
) AS SAPV ON First_Name = STUDENT_FIRST_NAME AND Last_Name = STUDENT_LAST_NAME
--(End 2)------------------------------------------------------------------------------------------------------------
ORDER BY Last_Name, First_Name