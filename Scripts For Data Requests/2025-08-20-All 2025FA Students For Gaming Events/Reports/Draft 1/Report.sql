--(Begin 1)-------------------------------------------------------------------------------------------------------------
SELECT DISTINCT ID,
       FIRST_NAME,
       LAST_NAME
FROM SPT_STUDENT_ACAD_CRED STC
JOIN ODS_PERSON PERSON ON STC.STC_PERSON_ID = PERSON.ID
WHERE STC_TERM = '2025FA'
AND CURRENT_STATUS_DESC IN ('New', 'Add')
AND STC_CRED_TYPE = 'INST'
--(End 1)---------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME