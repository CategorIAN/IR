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