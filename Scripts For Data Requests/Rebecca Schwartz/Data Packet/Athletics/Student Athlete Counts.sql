SELECT ENROLL_TERM AS TERM,
       COUNT(*) AS STUDENT_COUNT,
       SUM(STUDENT_ATHLETE) AS STUDENT_ATHLETE_COUNT
FROM (
SELECT DISTINCT ENROLL_TERM,
       TERM_START_DATE,
       STUDENT_ID,
       CASE
           WHEN EXISTS (
               SELECT 1
               FROM STA_OTHER_COHORTS_VIEW
               WHERE STA_STUDENT = STUDENT_ID
               AND STA_OTHER_COHORT_START_DATES < TERMS.TERM_END_DATE
               AND (STA_OTHER_COHORT_END_DATES > TERMS.TERM_START_DATE
                        OR STA_OTHER_COHORT_END_DATES IS NULL)
               AND STA_OTHER_COHORT_GROUPS IN (
                                               'F',
                                               'SOW',
                                               'SOM',
                                               'VB',
                                               'BM',
                                               'BW',
                                               'XW',
                                               'XM',
                                               'GW',
                                               'GM',
                                               'C',
                                               'D',
                                               'ITM',
                                               'ITW',
                                               'OTM',
                                               'OTW',
                                               'SB',
                                               'BWJ',
                                               'VBJ',
                                               'SOMJ',
                                               'BMJ',
                                               'DNC'
                                                )
           ) THEN 1 ELSE 0 END AS STUDENT_ATHLETE
FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN TERMS ON SEV.ENROLL_TERM = TERMS.TERMS_ID
WHERE TERMS.TERM_START_DATE >= DATEADD(year, -10, '2024-08-01')
AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
AND (ENROLL_TERM LIKE '%FA' OR ENROLL_TERM LIKE '%SP')
) AS X
GROUP BY ENROLL_TERM, TERM_START_DATE
ORDER BY TERM_START_DATE