--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN (DATEDIFF(YEAR, PERSON.BIRTH_DATE, TERM_START_DATE) >= 17)
                    AND (DATEDIFF(YEAR, PERSON.BIRTH_DATE, TERM_START_DATE) <= 19) THEN '17-19'
                  WHEN (DATEDIFF(YEAR, PERSON.BIRTH_DATE, TERM_START_DATE) >= 20) THEN '20 and Over' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
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
                  JOIN (VALUES ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                  JOIN PERSON ON COHORT.ID = PERSON.ID
                  WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
--(End 3)------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 CASE WHEN GENDER = 'M' THEN 'Male' WHEN GENDER = 'F' THEN 'Female' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
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
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                    JOIN PERSON ON COHORT.ID = PERSON.ID
         WHERE TERM_ORDER = 1
        AND GENDER IS NOT NULL
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
--(End 3)------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       'Pell' AS CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
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
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
         WHERE TERM_ORDER = 1
              AND EXISTS (
          SELECT 1
          FROM (
              SELECT SA_STUDENT_ID, AW_TERM
                FROM (
                      SELECT '2017FA' AS AW_TERM, *
                      FROM F17_AWARD_LIST) AS X
                WHERE SA_AWARD = 'FPELL'
                AND SA_ACTION = 'A'
               ) AS X
          WHERE COHORT.ID = SA_STUDENT_ID AND COHORT.TERM = AW_TERM
      )
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM
--(End 3)------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                 RACE.IPEDS_RACE_ETHNIC_DESC  AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
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
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
                    JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON COHORT.ID = RACE.ID
         WHERE TERM_ORDER = 1
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
--(End 3)------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
UNION
------------------------------------------------------------------------------------------------------------------------
--(Begin 3)---------------------------------------------------------------------------------
SELECT TERM,
       CATEGORY,
       SUM(CASE WHEN SIX_YEAR_GRADUATED = 1 THEN 0 ELSE 1 END) AS NOT_SIX_YEAR_GRADUATED,
       SUM(SIX_YEAR_GRADUATED) AS SIX_YEAR_GRADUATED,
       COUNT(*) AS TOTAL,
       AVG(1.0 * SIX_YEAR_GRADUATED) AS RATE
FROM (
--(Begin 2)---------------------------------------------------------------------------------
         SELECT DISTINCT COHORT.ID,
                COHORT.TERM,
                CASE WHEN STATE = 'MT' THEN 'In State' ELSE 'Out of State' END AS CATEGORY,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STUDENT_ID = COHORT.ID
                                   AND STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE >= COHORT.TERM_START_DATE
                                   AND STP_END_DATE < DATEADD(YEAR, 6, COHORT.TERM_START_DATE)) THEN 1
                    ELSE 0 END AS SIX_YEAR_GRADUATED
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
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
                    AND STC_CRED_TYPE IN ('INST')
--(End 1)---------------------------------------------------------------------------------------------------------
              ) AS COHORT
                  JOIN (VALUES
                               ('2017FA')) AS MY_TERMS(X) ON COHORT.TERM = X
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
--(End 2)------------------------------------------------------------------------------------
     ) AS X
GROUP BY TERM, CATEGORY
--(End 3)------------------------------------------------------------------------------------
