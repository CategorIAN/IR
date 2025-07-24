--(Begin 4)------------------------------------------------------------------------------------------------------
         SELECT PERIOD,
                AVG(1.0 * RETAINED) AS RETENTION_RATE
FROM (
--(Begin 3)------------------------------------------------------------------------------------------------------
         SELECT STUDENT_ID,
                PERIOD,
                CASE WHEN STAYED = 1 OR GRADUATED = 1 THEN 1 ELSE 0 END AS RETAINED
         FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
  SELECT STUDENT_ID,
         START_TERM + '-' + NEXT_TERM AS PERIOD,
         CASE
             WHEN EXISTS (SELECT 1
                          FROM STUDENT_ACAD_CRED AS STC_INNER
                                   LEFT JOIN STC_STATUSES AS STATUS_INNER
                                             ON STC_INNER.STUDENT_ACAD_CRED_ID =
                                                STATUS_INNER.STUDENT_ACAD_CRED_ID
                                                 AND STATUS_INNER.POS = 1
                                   LEFT JOIN STUDENT_COURSE_SEC AS SEC_INNER
                                             ON STC_INNER.STC_STUDENT_COURSE_SEC = SEC_INNER.STUDENT_COURSE_SEC_ID
                          WHERE STUDENT_ID = STC_INNER.STC_PERSON_ID
                            AND STC_INNER.STC_TERM = NEXT_TERM
                            AND STATUS_INNER.STC_STATUS IN ('N', 'A')
                            AND COALESCE(SEC_INNER.SCS_PASS_AUDIT, '') != 'A') THEN 1
             ELSE 0 END               AS STAYED,
         CASE
             WHEN EXISTS (SELECT 1
                          FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                          WHERE SAPV.STUDENT_ID = X.STUDENT_ID
                            AND STP_CURRENT_STATUS = 'Graduated'
                            AND (STP_END_DATE > START_TERM_START OR STP_END_DATE IS NULL))
                 THEN 1
             ELSE 0 END               AS GRADUATED
  FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
SELECT DISTINCT STC_PERSON_ID         AS STUDENT_ID,
           STC_TERM              AS START_TERM,
           TERMS.TERM_START_DATE AS START_TERM_START,
           PERSISTENCE.Y         AS NEXT_TERM
FROM STUDENT_ACAD_CRED AS STC
    LEFT JOIN STC_STATUSES AS STATUS
              ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND
                 STATUS.POS = 1
    LEFT JOIN STUDENT_COURSE_SEC AS SEC
              ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
    JOIN (VALUES ('2018FA', '2019FA'),
                 ('2019FA', '2020FA'),
                 ('2020FA', '2021FA'),
                 ('2021FA', '2022FA'),
                 ('2022FA', '2023FA'),
                 ('2023FA', '2024FA')) AS PERSISTENCE(X, Y) ON STC.STC_TERM = X
    JOIN TERMS ON STC.STC_TERM = TERMS_ID
WHERE STATUS.STC_STATUS IN ('N', 'A')
AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
--(End 1)--------------------------------------------------------------------------------------------------------------
                       ) AS X
--(End 2)-------------------------------------------------------------------------------------------------------
              ) AS X
--(End 3)-------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY PERIOD
--(End 4)-------------------------------------------------------------------------------------------------------