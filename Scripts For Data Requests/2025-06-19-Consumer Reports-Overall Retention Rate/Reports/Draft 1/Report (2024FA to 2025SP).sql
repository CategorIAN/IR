--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(1.0 * RETURNED), 'P') AS RATE
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT COHORT.ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                   AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                                   AND ENROLL_TERM = '2025SP') THEN 1
                    ELSE 0 END AS RETURNED
         FROM (
---------------------------------------------------COHORT---------------------------------------------------------------
                  SELECT ID,
                         TERM
                  FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                        APPL_START_TERM                                                          AS TERM,
                                        TERM_START_DATE,
                                        ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                        FROM APPLICATIONS AS AP
                                 JOIN STUDENT_ACAD_CRED AS AC
                                      ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                 JOIN STC_STATUSES AS STAT
                                      ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                 JOIN TERMS ON APPL_START_TERM = TERMS_ID
                        WHERE APPL_DATE IS NOT NULL
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
                          AND STC_STATUS IN ('A', 'N')
                          AND STC_CRED_TYPE IN ('INST')
                          ----------FFUG------------------
                        AND APPL_STUDENT_TYPE = 'UG'
                        AND APPL_STUDENT_LOAD_INTENT = 'F'
                        AND APPL_ADMIT_STATUS = 'FY'
                 ) AS X
                  WHERE TERM_ORDER = 1
------------------------------------------------------------------------------------------------------------------------
              ) AS COHORT
------------------------------------------------------------------------------------------------------------------------
         WHERE TERM = '2024FA'
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------