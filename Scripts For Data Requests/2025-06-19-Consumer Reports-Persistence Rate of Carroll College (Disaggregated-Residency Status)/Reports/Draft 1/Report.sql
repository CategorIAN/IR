SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN PERSISTED = 1 THEN 0 ELSE 1 END) AS NOT_PERSISTED,
       SUM(PERSISTED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * PERSISTED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT DISTINCT COHORT.ID,
             COHORT.TERM,
             CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
             CASE
                 WHEN EXISTS (SELECT 1
                              FROM STUDENT_ENROLLMENT_VIEW
                              WHERE STUDENT_ID = COHORT.ID
                                AND ENROLL_TERM = NEXT_TERM.Y
                                AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)) THEN 1
                 ELSE 0 END AS PERSISTED
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
                            ('2023FA', '2024SP')) AS NEXT_TERM(X, Y) ON TERM = X
                JOIN (
                    SELECT ID,
                           STATE
                    FROM (SELECT ID,
                                 PAV.STATE,
                                 ROW_NUMBER() OVER (PARTITION BY ID ORDER BY ADDRESS_ADD_DATE) AS RANK
                          FROM PERSON_ADDRESSES_VIEW AS PAV
                                   JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
                          WHERE ADDRESS_TYPE = 'H') AS X
                    WHERE RANK = 1
                ) AS STUDENT_STATE ON COHORT.ID = STUDENT_STATE.ID
      WHERE TERM_ORDER = 1
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
