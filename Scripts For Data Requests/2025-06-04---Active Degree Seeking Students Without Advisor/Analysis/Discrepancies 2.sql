SELECT DEGREE_STATUS,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STPR_STUDENT AS ID,
                FIRST_NAME,
                LAST_NAME,
                CASE WHEN (TITLE = 'Continuing Education' OR TITLE = 'Non-Degree Seeking Students') THEN TITLE
                ELSE 'Degree-Seeking' END AS DEGREE_STATUS
         FROM ODS_STUDENT_PROGRAMS AS SP
         LEFT JOIN Z01_PERSON ON SP.STPR_STUDENT = ID
         WHERE CURRENT_STATUS_DESC = 'Active'
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY DEGREE_STATUS




SELECT STPR_STUDENT AS ID
FROM ODS_STUDENT_PROGRAMS AS OSP
WHERE CURRENT_STATUS_DESC = 'Active'
AND TITLE NOT IN ('Continuing Education', 'Non-Degree Seeking Students')
EXCEPT
SELECT STTR_STUDENT AS ID
FROM ODS_STUDENT_TERMS AS OST
WHERE STTR_TERM IN ('2025SP', '2025FA', '2025SU')

--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SELECT DISTINCT OSP.STPR_STUDENT
FROM ODS_STUDENT_PROGRAMS AS OSP
WHERE CURRENT_STATUS_DESC = 'Active'
AND TITLE NOT IN ('Continuing Education', 'Non-Degree Seeking Students')
AND NOT EXISTS (
SELECT 1
FROM ODS_STUDENT_TERMS AS OST
WHERE STTR_TERM IN ('2025SP', '2025FA', '2025SU')
AND OST.STTR_STUDENT = OSP.STPR_STUDENT
)

SELECT DISTINCT OST.STTR_STUDENT
FROM ODS_STUDENT_TERMS AS OST
WHERE STTR_TERM IN ('2025SP', '2025FA', '2025SU')
AND NOT EXISTS (
    SELECT 1
    FROM ODS_STUDENT_PROGRAMS AS OSP
    WHERE CURRENT_STATUS_DESC = 'Active'
    AND TITLE NOT IN ('Continuing Education', 'Non-Degree Seeking Students')
    AND OST.STTR_STUDENT = OSP.STPR_STUDENT
)

--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SELECT DISTINCT OSP.STPR_STUDENT
FROM ODS_STUDENT_PROGRAMS AS OSP
WHERE CURRENT_STATUS_DESC = 'Active'
AND TITLE NOT IN ('Continuing Education', 'Non-Degree Seeking Students')
AND NOT EXISTS (
SELECT 1
FROM Z01_STUDENT_COURSE_SEC AS SCS
WHERE SCS.SCS_TERM IN ('2025SP', '2025FA', '2025SU')
AND SCS.SCS_STUDENT = OSP.STPR_STUDENT
)


SELECT DISTINCT SCS.SCS_STUDENT
FROM Z01_STUDENT_COURSE_SEC AS SCS
WHERE SCS.SCS_TERM IN ('2025SP', '2025FA', '2025SU')
AND NOT EXISTS (
    SELECT 1
    FROM ODS_STUDENT_PROGRAMS AS OSP
    WHERE CURRENT_STATUS_DESC = 'Active'
    AND TITLE NOT IN ('Continuing Education', 'Non-Degree Seeking Students')
    AND SCS.SCS_STUDENT = OSP.STPR_STUDENT
)







