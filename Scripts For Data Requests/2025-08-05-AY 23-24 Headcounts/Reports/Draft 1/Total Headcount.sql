--(Begin 1)-------------------------------------------------------------------------------------------------------------
SELECT COUNT(DISTINCT STC.STC_PERSON_ID) AS [Unduplicated Student Count]
FROM STUDENT_ACAD_CRED AS STC
LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
AND STATUS.STC_STATUS IN ('N', 'A')
AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
AND STC.STC_CRED > 0
AND STC.STC_CRED_TYPE = 'INST'
--(End 1)---------------------------------------------------------------------------------------------------------------