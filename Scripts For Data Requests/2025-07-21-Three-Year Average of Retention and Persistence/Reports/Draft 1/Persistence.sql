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
--(Begin 1)-------------------------------------------------------------------------------------------------------------
SELECT DISTINCT STC_PERSON_ID AS STUDENT_ID,
       STC_TERM AS START_TERM,
        PERSISTENCE.Y AS NEXT_TERM,
        CASE WHEN EXISTS (
            SELECT 1
            FROM STUDENT_ACAD_CRED AS STC_INNER
            LEFT JOIN STC_STATUSES AS STATUS_INNER ON STC_INNER.STUDENT_ACAD_CRED_ID = STATUS_INNER.STUDENT_ACAD_CRED_ID
                                                          AND STATUS_INNER.POS = 1
            LEFT JOIN STUDENT_COURSE_SEC AS SEC_INNER
                ON STC_INNER.STC_STUDENT_COURSE_SEC = SEC_INNER.STUDENT_COURSE_SEC_ID
            WHERE STC.STC_PERSON_ID = STC_INNER.STC_PERSON_ID
            AND STC_INNER.STC_TERM = PERSISTENCE.Y
            AND STATUS_INNER.STC_STATUS IN ('N', 'A')
            AND COALESCE(SEC_INNER.SCS_PASS_AUDIT, '') != 'A'
        ) THEN 1 ELSE 0 END AS STAYED,
       CASE
       WHEN EXISTS (SELECT 1
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    WHERE SAPV.STUDENT_ID = STC.STC_PERSON_ID
                      AND STP_CURRENT_STATUS = 'Graduated'
                      AND (STP_END_DATE > TERMS.TERM_START_DATE OR STP_END_DATE IS NULL))
           THEN 1
       ELSE 0 END AS GRADUATED

FROM STUDENT_ACAD_CRED AS STC
LEFT JOIN STC_STATUSES AS STATUS ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND STATUS.POS = 1
LEFT JOIN STUDENT_COURSE_SEC AS SEC ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
JOIN (VALUES ('2022FA', '2023SP'),
             ('2023FA', '2024SP'),
             ('2024FA', '2025SP')) AS PERSISTENCE(X, Y) ON STC.STC_TERM = X
JOIN TERMS ON STC.STC_TERM = TERMS_ID
WHERE STATUS.STC_STATUS IN ('N', 'A')
AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
--(End 1)--------------------------------------------------------------------------------------------------------------
                       ) AS X
--(End 2)-------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY PERIOD
--(End 3)-------------------------------------------------------------------------------------------------------
     ) AS X
--(End 4)-------------------------------------------------------------------------------------------------------