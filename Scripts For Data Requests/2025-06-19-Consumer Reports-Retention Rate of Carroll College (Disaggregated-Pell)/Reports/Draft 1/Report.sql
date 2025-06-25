--(Begin 2)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN RETAINED = 1 THEN 0 ELSE 1 END) AS NOT_RETAINED,
       SUM(RETAINED) AS RETAINED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * RETAINED) AS RATE
--(Begin 1)---------------------------------------------------------------------------------
FROM (SELECT COHORT.ID,
             COHORT.TERM,
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
      WHERE TERM_ORDER = 1
      AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2023FA' AS AW_TERM, *
                      FROM F23_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
--(End 1)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 2)------------------------------------------------------------------------------------
