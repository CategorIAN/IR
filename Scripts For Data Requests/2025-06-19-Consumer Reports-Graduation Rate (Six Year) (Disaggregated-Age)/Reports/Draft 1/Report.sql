--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN FOUR_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_FOUR_YEAR_GRADUATED,
       SUM(FOUR_YEAR_GRADUATED) AS PERSISTED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * FOUR_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN (STUDENT_AGE >= (17 + DATEDIFF(YEAR, 2017, 2024)) AND STUDENT_AGE <= + DATEDIFF(YEAR, 2017, 2024)) THEN '17-19'
                  WHEN (STUDENT_AGE >= 20) THEN '20 and Over' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 4, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
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
                  JOIN (VALUES
                               ('2015FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                    JOIN STUDENT_ENROLLMENT_VIEW ON COHORT.ID = STUDENT_ID
         WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY