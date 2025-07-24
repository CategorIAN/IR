--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT School,
       Year,
       CAST(AVG(1.0 * FOUR_YEAR_GRADUATED) * 100 AS INT) AS [Graduation Rate (4 Years, Pell, Men)]
         FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                  SELECT School,
                         Year,
                         COHORT.ID                                                        AS STUDENT_ID,
                         CASE
                            WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE < DATEADD(YEAR, 4, TERMS.TERM_START_DATE)
                                   AND STUDENT_ID = COHORT.ID) THEN 1
                    ELSE 0 END AS FOUR_YEAR_GRADUATED
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
                           JOIN TERMS
                                ON CAST(YEARS.Year AS INT) - 8 = TERMS.TERM_REPORTING_YEAR
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
                                         ) AS X
                                 WHERE TERM_ORDER = 1) AS COHORT ON TERMS.TERMS_ID = COHORT.TERM
                  JOIN  (
                        SELECT '2007FA' AS AW_TERM, *
                        FROM F07_AWARD_LIST
                        UNION
                        SELECT '2008FA' AS AW_TERM, *
                        FROM F08_AWARD_LIST
                        UNION
                        SELECT '2009FA' AS AW_TERM, *
                        FROM F09_AWARD_LIST
                        UNION
                        SELECT '2010FA' AS AW_TERM, *
                        FROM F10_AWARD_LIST
                        UNION
                        SELECT '2011FA' AS AW_TERM, *
                        FROM F11_AWARD_LIST
                        UNION
                        SELECT '2012FA' AS AW_TERM, *
                        FROM F12_AWARD_LIST
                        UNION
                        SELECT '2013FA' AS AW_TERM, *
                        FROM F13_AWARD_LIST
                        UNION
                        SELECT '2014FA' AS AW_TERM, *
                        FROM F14_AWARD_LIST
                        UNION
                        SELECT '2015FA' AS AW_TERM, *
                        FROM F15_AWARD_LIST
                        UNION
                        SELECT '2016FA' AS AW_TERM, *
                        FROM F16_AWARD_LIST
                        UNION
                        SELECT '2017FA' AS AW_TERM, *
                        FROM F17_AWARD_LIST
                        UNION
                        SELECT '2018FA', *
                        FROM F18_AWARD_LIST
                        UNION
                        SELECT '2019FA', *
                        FROM F19_AWARD_LIST
                        UNION
                        SELECT '2020FA', *
                        FROM F20_AWARD_LIST
                        UNION
                        SELECT '2021FA', *
                        FROM F21_AWARD_LIST
                        UNION
                        SELECT '2022FA', *
                        FROM F22_AWARD_LIST
                ) AS PELL ON PELL.SA_ACTION = 'A'
                      AND PELL.SA_AWARD = 'FPELL'
                      AND PELL.AW_TERM = COHORT.TERM
                      AND PELL.SA_STUDENT_ID = COHORT.ID
                  JOIN PERSON ON PERSON.ID = COHORT.ID
                  WHERE PERSON.GENDER = 'M'
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
GROUP BY School, Year
--(End 2)---------------------------------------------------------------------------------------------------------------