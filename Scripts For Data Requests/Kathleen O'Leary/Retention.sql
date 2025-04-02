SELECT ID,
       CASE WHEN EXISTS (
           SELECT 1
           FROM STUDENT_ENROLLMENT_VIEW
           WHERE ENROLL_TERM = '2024FA'
           AND STUDENT_ID = ID
           AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
           AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
           AND ENROLL_CREDITS > 0
       ) THEN 1 ELSE 0 END AS STILL_ENROLLED
FROM Z01_AAV_STUDENT_FIRST_MATRIC AS FM
JOIN (SELECT STPR_STUDENT
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
               ) AS X
               WHERE ADMIT_RANK = 1
               AND STPR_ADMIT_STATUS = 'FY'
               ) AS FIRST_ADMIT ON FM.ID = FIRST_ADMIT.STPR_STUDENT
WHERE FM.TERM = '2023FA'
---------------------------------------------------------------------------------------------------------------------