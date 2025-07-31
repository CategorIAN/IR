--(Begin 2)------------------------------------------------------------------------------------------
SELECT GENDER,
       FORMAT(1.0 * COUNT(*) / TOTAL, 'P') AS [PERCENT]
FROM (
--(Begin 1)------------------------------------------------------------------------------------------
         SELECT DISTINCT STUDENT_ID,
                         CASE
                             WHEN GENDER = 'M' THEN 'Male'
                             WHEN GENDER = 'F' THEN 'Female'
                             ELSE 'Other' END AS GENDER,
                         COUNT(*) OVER ()     AS TOTAL
         FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  JOIN PERSON ON SAPV.STUDENT_ID = PERSON.ID
         WHERE STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND STP_START_DATE <= '2024-07-01'
           AND COALESCE(STP_END_DATE, GETDATE()) >= '2024-07-01'
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
           AND (STP_CURRENT_STATUS NOT IN ('Not Returned', 'Changed Program') OR STP_CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)--------------------------------------------------------------------------------------------
     ) AS X
GROUP BY GENDER, TOTAL
--(End 2)--------------------------------------------------------------------------------------------