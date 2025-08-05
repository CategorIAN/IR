--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT TERM,
       COUNT(*) AS [Undergraduate FT Headcount]
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STC_TERM          AS TERM,
                         TERM_START_DATE,
                         STC.STC_PERSON_ID AS ID
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  LEFT JOIN STUDENT_TERMS
                            ON STUDENT_TERMS_ID = STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL
                  LEFT JOIN TERMS ON STC_TERM = TERMS_ID
         WHERE STC_TERM IN ('2023FA', '2024SP', '2024SU')
           AND STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC.STC_CRED > 0
           AND STC.STC_CRED_TYPE = 'INST'
           AND STC.STC_ACAD_LEVEL = 'UG'
           AND STUDENT_TERMS.STTR_STUDENT_LOAD IN ('F', 'O')
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, TERM_START_DATE
--(End 2)---------------------------------------------------------------------------------------------------------------
ORDER BY TERM_START_DATE