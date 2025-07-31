--(Begin 2)------------------------------------------------------------------------------------------
SELECT CAST(ROUND(AVG(1.0 * AGE), 0) AS INT) AS AVERAGE_AGE
FROM (
--(Begin 1)------------------------------------------------------------------------------------------
         SELECT DISTINCT STUDENT_ID,
                CAST(DATEDIFF(DAY, BIRTH_DATE, '2024-07-01') / 365.25 AS INT) AS AGE
         FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  JOIN PERSON ON SAPV.STUDENT_ID = PERSON.ID
         WHERE STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND STP_START_DATE <= '2024-07-01'
           AND COALESCE(STP_END_DATE, GETDATE()) >= '2024-07-01'
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
            AND (STP_CURRENT_STATUS NOT IN ('Not Returned', 'Changed Program') OR STP_CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)--------------------------------------------------------------------------------------------
     ) AS X
--(End 2)--------------------------------------------------------------------------------------------


SELECT *
FROM STUDENT_TERMS_VIEW
