--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT CAST(ROUND(AVG(1.0 * AGE), 0) AS INT) AS AVERAGE_AGE
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STPR_STUDENT,
                         CAST(DATEDIFF(DAY, BIRTH_DATE, '2024-07-01') / 365.25 AS INT) AS AGE
         FROM SPT_STUDENT_PROGRAMS AS SP
                  JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
                  JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
         WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND SP.START_DATE <= '2024-07-01'
           AND COALESCE(SP.END_DATE, GETDATE()) >= '2024-07-01'
           AND CURRENT_STATUS_DESC != 'Did Not Enroll'
           AND (CURRENT_STATUS_DESC NOT IN ('Not Returned', 'Changed Program') OR CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------


SELECT *
FROM SPT_STUDENT_PROGRAMS AS SP
JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
AND SP.START_DATE <= '2024-07-01'


--(Begin 3)----------------------------------------------------------------------------------
SELECT STUDENT_ID,
       STPR_STUDENT,
       FIRST_NAME,
       LAST_NAME,
       ACPG_TITLE,
       START_DATE,
       END_DATE
FROM (
--(Begin 2)-----------------------------------------------------------------------------------
         SELECT STUDENT_ID,
                MAX(CASE WHEN PROGRAM = 'Nursing' THEN 1 ELSE 0 END)     AS NURSING,
                MAX(CASE WHEN PROGRAM = 'Pre-Nursing' THEN 1 ELSE 0 END) AS PRE_NURSING
         FROM (
--(Begin 1)------------------------------------------------------------------------------------
                  SELECT STUDENT_PROGRAMS_ID,
                         STPR_STUDENT AS STUDENT_ID,
                         FIRST_NAME,
                         LAST_NAME,
                         ACPG_TITLE   AS PROGRAM,
                         START_DATE,
                         END_DATE
                  FROM SPT_STUDENT_PROGRAMS AS SP
                           JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
                           JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
                  WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing', 'Pre-Nursing')
--(End 1)--------------------------------------------------------------------------------------
              ) AS X
         GROUP BY STUDENT_ID
--(End 2)--------------------------------------------------------------------------------------
     ) AS X
    JOIN SPT_STUDENT_PROGRAMS AS SP ON X.STUDENT_ID = SP.STPR_STUDENT
                           JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
                           JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
WHERE NURSING = 1 AND PRE_NURSING = 1
AND ACPG_TITLE IN ('Nursing', 'Pre-Nursing')
--(End 3)--------------------------------------------------------------------------------------
ORDER BY STUDENT_ID, ACPG_TITLE DESC