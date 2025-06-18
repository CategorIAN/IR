SELECT *,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STPR_STUDENT AS ID,
                FIRST_NAME,
                LAST_NAME
         FROM ODS_STUDENT_PROGRAMS AS SP
         LEFT JOIN Z01_PERSON ON SP.STPR_STUDENT = ID
         WHERE
             TITLE != 'Continuing Education'
            AND TITLE != 'Non-Degree Seeking Students'
            AND NOT EXISTS (SELECT 1
                           FROM ODS_STUDENT_ADVISEMENT
                           WHERE STAD_STUDENT = STPR_STUDENT
                             AND STAD_END_DATE IS NULL)
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY ID, FIRST_NAME, LAST_NAME, TITLE
HAVING COUNT(*) > 1