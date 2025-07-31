--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT ACAD_LEVEL,
       COUNT(*) AS UNDUPLICATED_HEADCOUNT
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT LEFT(STC_STUDENT_ACAD_LEVELS_ID, 7) AS STUDENT_ID,
                         SPT_STUDENT_ACAD_CRED.ACAD_LEVEL_DESC AS ACAD_LEVEL
         FROM SPT_STUDENT_ACAD_CRED
         WHERE STC_START_DATE >= '2024-07-01'
           AND STC_END_DATE < '2025-07-01'
           AND STC_CRED_TYPE = 'INST'
           AND CURRENT_STATUS_DESC IN ('New', 'Add')
           AND STC_GRADE != 'Audit'
           AND STC_CRED > 0
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY ACAD_LEVEL
--(End 2)---------------------------------------------------------------------------------------------------------------