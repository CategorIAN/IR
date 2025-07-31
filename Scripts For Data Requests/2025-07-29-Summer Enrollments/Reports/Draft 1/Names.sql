--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT
                DISTINCT COURSES.CRS_NAME AS COURSE,
                STC_TERM AS TERM,
                STC_PERSON_ID,
                FIRST_NAME,
                LAST_NAME
         FROM STUDENT_ACAD_CRED AS STC
                  LEFT JOIN STC_STATUSES AS STATUS
                            ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
                  LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                    LEFT JOIN COURSES ON STC.STC_COURSE = COURSES_ID
                    LEFT JOIN PERSON ON STC_PERSON_ID = PERSON.ID
         WHERE STATUS.STC_STATUS IN ('N', 'A')
           AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
           AND STC_CRED_TYPE = 'INST'
           AND STC_START_DATE BETWEEN DATEADD(YEAR, -5, '2025-01-01') AND '2025-01-01'
           AND STC_TERM LIKE '%SU'
--(End 1)---------------------------------------------------------------------------------------------------------------
ORDER BY COURSE, TERM, LAST_NAME
