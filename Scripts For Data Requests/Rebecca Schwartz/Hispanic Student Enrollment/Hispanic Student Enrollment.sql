--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT TERM,
        COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                         TERMS.TERM_START_DATE,
                         STUDENT_ID,
                         STUDENT_LAST_NAME,
                         STUDENT_FIRST_NAME
         FROM STUDENT_ENROLLMENT_VIEW AS SEV
                  JOIN TERMS ON SEV.ENROLL_TERM = TERMS.TERMS_ID
                  JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON SEV.STUDENT_ID = RACE.ID
         WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, GETDATE())
           AND TERMS.TERM_END_DATE < '2025-06-01'
           AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
           AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
           AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
           AND RACE.IPEDS_RACE_ETHNIC_DESC = 'Hispanic/Latino'
--(End 1)------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, TERM_START_DATE
--(End 2)------------------------------------------------------------------------------------------------------------
ORDER BY TERM_START_DATE