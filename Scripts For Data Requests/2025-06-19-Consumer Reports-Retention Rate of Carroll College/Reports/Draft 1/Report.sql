--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       AVG(1.0 * RETAINED) AS RETENTION_RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
      SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
-------------------------------------------------------------------------------------------------------------------
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
) AS COHORT
               JOIN (VALUES ('2021FA', '2022FA'),
                            ('2022FA', '2023FA'),
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM

--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       AVG(1.0 * RETAINED) AS RETENTION_RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
      SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
-------------------------------------------------------------------------------------------------------------------
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
                        AND APPL_STUDENT_TYPE = 'UG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
) AS COHORT
               JOIN (VALUES ('2021FA', '2022FA'),
                            ('2022FA', '2023FA'),
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM

--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       AVG(1.0 * RETAINED) AS RETENTION_RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
      SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
-------------------------------------------------------------------------------------------------------------------
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
                        AND APPL_ADMIT_STATUS = 'FY'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
) AS COHORT
               JOIN (VALUES ('2021FA', '2022FA'),
                            ('2022FA', '2023FA'),
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM

--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       AVG(1.0 * RETAINED) AS RETENTION_RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
SELECT COHORT.ID,
             COHORT.TERM,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
      SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
-------------------------------------------------------------------------------------------------------------------
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
                        AND APPL_STUDENT_LOAD_INTENT IN ('F', 'O')
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
) AS COHORT
               JOIN (VALUES ('2021FA', '2022FA'),
                            ('2022FA', '2023FA'),
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
      WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM




SELECT *
FROM APPLICATIONS
