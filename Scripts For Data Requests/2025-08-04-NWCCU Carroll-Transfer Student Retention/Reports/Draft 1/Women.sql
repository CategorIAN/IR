--(Begin 3)------------------------------------------------------------------------------------------------------------
SELECT School,
       Year,
       CAST(AVG(1.0 * STAYED) * 100 AS INT) AS [Retention Rate (Transfers, Women)]
FROM (
--(Begin 2)------------------------------------------------------------------------------------------------------------
         SELECT School,
                Year,
                STUDENT_ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_CRED AS STC
                                          LEFT JOIN STC_STATUSES AS STATUS
                                                    ON STC.STUDENT_ACAD_CRED_ID = STATUS.STUDENT_ACAD_CRED_ID AND
                                                       STATUS.POS = 1
                                          LEFT JOIN STUDENT_COURSE_SEC AS SEC
                                                    ON STC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                                 WHERE STATUS.STC_STATUS IN ('N', 'A')
                                   AND COALESCE(SEC.SCS_PASS_AUDIT, '') != 'A'
                                     -----
                                    AND STC_CRED_TYPE = 'INST'
                                   --------------------------------------------------------
                                   AND STC.STC_PERSON_ID = X.STUDENT_ID
                                   AND STC.STC_TERM = X.NEXT_TERM) THEN 1
                    ELSE 0 END AS STAYED
         FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                  SELECT School,
                         Year,
                         COHORT.ID                                                        AS STUDENT_ID,
                         CAST(CAST(LEFT(START_TERM.TERMS_ID, 4) AS INT) + 1 AS VARCHAR) + 'FA' AS NEXT_TERM
                  FROM (VALUES ('Carroll College')) AS SCHOOLS(School)
                           CROSS JOIN (VALUES (2015),
                                              (2016),
                                              (2017),
                                              (2018),
                                              (2019),
                                              (2020),
                                              (2021),
                                              (2022),
                                              (2023)) AS YEARS(Year)
                           JOIN TERMS AS START_TERM
                                ON CAST(YEARS.Year AS INT) - 1 = START_TERM.TERM_REPORTING_YEAR
                                    AND SUBSTRING(TERMS_ID, 5, 6) = 'FA'
                           JOIN (SELECT X.ID, X.TERM
                                 FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                                       APPL_START_TERM                                                          AS TERM,
                                                       ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                                       FROM APPLICATIONS AS AP
                                                JOIN STUDENT_ACAD_CRED AS AC
                                                     ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND
                                                        AP.APPL_START_TERM = AC.STC_TERM
                                                JOIN STC_STATUSES AS STAT
                                                     ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                                JOIN TERMS ON APPL_START_TERM = TERMS_ID
                                       WHERE APPL_DATE IS NOT NULL
                                         AND STC_STATUS IN ('A', 'N')
                                         AND STC_CRED_TYPE IN ('INST')
                                         --FFUG--
                                         AND APPL_STUDENT_TYPE = 'UG'
                                         AND APPL_STUDENT_LOAD_INTENT = 'F'
                                         AND APPL_ADMIT_STATUS = 'TR') AS X
                                 WHERE TERM_ORDER = 1) AS COHORT ON START_TERM.TERMS_ID = COHORT.TERM
                        JOIN PERSON ON COHORT.ID = PERSON.ID
                  WHERE PERSON.GENDER = 'F'
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY School, Year
--(End 3)---------------------------------------------------------------------------------------------------------------