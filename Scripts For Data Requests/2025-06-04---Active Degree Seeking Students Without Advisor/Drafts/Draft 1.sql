--(Begin 1)-------------------------------------------------------------------------------------------------------------
SELECT DISTINCT STPR_STUDENT AS ID,
       FIRST_NAME,
       LAST_NAME
FROM ODS_STUDENT_PROGRAMS AS SP
LEFT JOIN Z01_PERSON ON SP.STPR_STUDENT = ID
WHERE CURRENT_STATUS_DESC = 'Active'
AND TITLE != 'Continuing Education'
AND TITLE != 'Non-Degree Seeking Students'
AND NOT EXISTS (
    SELECT 1
    FROM ODS_STUDENT_ADVISEMENT
    WHERE STAD_STUDENT = STPR_STUDENT
    AND (STAD_END_DATE IS NULL OR STAD_END_DATE > GETDATE())
)
AND STPR_STUDENT IN ('6192308', '6187660', '6174382')
--(End 1)---------------------------------------------------------------------------------------------------------------
ORDER BY ID

SELECT *
FROM DBO_RHC_ADVISOR
WHERE STAD_STUDENT = '6187660'


SELECT *
FROM ODS_STUDENT_ADVISEMENT
WHERE STAD_STUDENT = '6187660'

SELECT *
FROM Z01_STUDENT_ADVISEMENT
