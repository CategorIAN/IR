--(Begin 4)------------------------------------------------------------------------------------------------------
SELECT AVG(PERSISTENCE_RATE) AS THREE_YEAR_AVG_PERSISTENCE_RATE
FROM (
--(Begin 3)------------------------------------------------------------------------------------------------------
         SELECT PERIOD,
                AVG(1.0 * PERSISTED) AS PERSISTENCE_RATE
         FROM (
--(Begin 2)------------------------------------------------------------------------------------------------------
                  SELECT STUDENT_ID,
                         START_TERM + '-' + NEXT_TERM                            AS PERIOD,
                         CASE WHEN STAYED = 1 OR GRADUATED = 1 THEN 1 ELSE 0 END AS PERSISTED
                  FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------
                           SELECT DISTINCT STUDENT_ID,
                                           ENROLL_TERM    AS START_TERM,
                                           PERSISTENCE.Y  AS NEXT_TERM,
                                           CASE
                                               WHEN EXISTS (SELECT 1
                                                            FROM STUDENT_ENROLLMENT_VIEW AS SEV_INNER
                                                            WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                                              AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                                                              AND SEV_INNER.STUDENT_ID = SEV.STUDENT_ID
                                                              AND SEV_INNER.ENROLL_TERM = PERSISTENCE.Y) THEN 1
                                               ELSE 0 END AS STAYED,
                                           CASE
                                               WHEN EXISTS (SELECT 1
                                                            FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                            WHERE SAPV.STUDENT_ID = SEV.STUDENT_ID
                                                              AND STP_CURRENT_STATUS = 'Graduated'
                                                              AND (STP_END_DATE > TERMS.TERM_START_DATE OR STP_END_DATE IS NULL))
                                                   THEN 1
                                               ELSE 0 END AS GRADUATED
                           FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                    JOIN (VALUES ('2022FA', '2023SP'),
                                                 ('2023FA', '2024SP'),
                                                 ('2024FA', '2025SP')) AS PERSISTENCE(X, Y) ON SEV.ENROLL_TERM = X
                                    JOIN TERMS ON SEV.ENROLL_TERM = TERMS_ID
                           WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
                             AND COALESCE(ENROLL_SCS_PASS_AUDIT, '') != 'A'
                             AND ENROLL_TERM IN ('2022FA', '2023FA', '2024FA')
--(End 1)-------------------------------------------------------------------------------------------------------
                       ) AS X
--(End 2)-------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY PERIOD
--(End 3)-------------------------------------------------------------------------------------------------------
     ) AS X
--(End 4)-------------------------------------------------------------------------------------------------------