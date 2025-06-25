SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             RACE.IPEDS_RACE_ETHNIC_DESC AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS RETAINED
      FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                            APPL_START_TERM                                                          AS TERM,
                            TERM_START_DATE,
                            ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
            FROM APPLICATIONS AS AP
                     JOIN STUDENT_ACAD_CRED AS AC
                          ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                     JOIN STC_STATUSES AS STAT ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                     JOIN TERMS ON APPL_START_TERM = TERMS_ID
                    WHERE APPL_DATE IS NOT NULL
                    AND APPL_ACAD_PROGRAM != 'NDEG'
--     AND APPL_WITHDRAW_DATE IS NULL (Should not use)
              AND STC_STATUS IN ('A', 'N')
              AND STC_CRED_TYPE IN ('INST')) AS COHORT
               JOIN (VALUES
                            ('2023FA', '2024FA')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON RACE.ID = COHORT.ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY

