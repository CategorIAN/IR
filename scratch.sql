--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT LOAD,
       COUNT(*) AS STUDENTS
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STUDENT_ID,
                         LOADS.NAME AS LOAD
         FROM STUDENT_ACAD_CRED AS STC
                  JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND POS = 1
                  JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON STC.STC_PERSON_ID = SAPV.STUDENT_ID
                  JOIN STUDENT_TERMS_VIEW AS STV ON STC_PERSON_ID = STV.STTR_STUDENT AND STC_TERM = STV.STTR_TERM
                  JOIN (VALUES ('F', 'Full-Time'),
                               ('O', 'Full-Time'),
                               ('L', 'Part-Time')) AS LOADS(ID, NAME) ON STV.STTR_STUDENT_LOAD = LOADS.ID
         WHERE STC_TERM = '2025FA'
           AND STP_START_DATE <= STC_END_DATE
           AND COALESCE(STP_END_DATE, STC_START_DATE) >= STC_START_DATE
           AND STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND STC_STATUS IN ('N', 'A')
           AND COALESCE(SCS_PASS_AUDIT, '') != 'A'
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY LOAD
--(End 2)---------------------------------------------------------------------------------------------------------------

SELECT STUDENT_ID
FROM STUDENT_ACAD_PROGRAMS_VIEW

SELECT *
FROM STUDENT_TERMS_VIEW
