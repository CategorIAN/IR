--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT School,
       Year,
       CAST(AVG(1.0 * GRADUATED) * 100 AS INT) AS [Graduation Rate (6 Years, Athlete, Men)]
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT School,
                Year,
                COHORT.ID,
                CASE
                    WHEN EXISTS (SELECT 1
                                 FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                 WHERE STP_CURRENT_STATUS = 'Graduated'
                                   AND STP_END_DATE < DATEADD(YEAR, 6, START_TERM.TERM_START_DATE)
                                   AND STUDENT_ID = COHORT.ID) THEN 1
                    ELSE 0 END AS GRADUATED
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
                       ON CAST(YEARS.Year AS INT) - 8 = START_TERM.TERM_REPORTING_YEAR
                           AND SUBSTRING(TERMS_ID, 5, 6) = 'FA'
                  JOIN (SELECT X.ID, X.TERM
                        FROM (SELECT DISTINCT APPL_APPLICANT                                                           AS ID,
                                              APPL_START_TERM                                                          AS TERM,
                                              ROW_NUMBER() OVER (PARTITION BY APPL_APPLICANT ORDER BY TERM_START_DATE) AS TERM_ORDER
                              FROM APPLICATIONS AS AP
                                       JOIN STUDENT_ACAD_CRED AS AC
                                            ON AP.APPL_APPLICANT = AC.STC_PERSON_ID AND AP.APPL_START_TERM = AC.STC_TERM
                                       JOIN STC_STATUSES AS STAT
                                            ON AC.STUDENT_ACAD_CRED_ID = STAT.STUDENT_ACAD_CRED_ID AND POS = 1
                                       JOIN TERMS ON APPL_START_TERM = TERMS_ID
                              WHERE APPL_DATE IS NOT NULL
                                AND STC_STATUS IN ('A', 'N')
                                AND STC_CRED_TYPE IN ('INST')) AS X
                        WHERE TERM_ORDER = 1) AS COHORT ON START_TERM.TERMS_ID = COHORT.TERM
         JOIN PERSON ON COHORT.ID = PERSON.ID
         WHERE EXISTS (SELECT 1
                       FROM STA_OTHER_COHORTS_VIEW
                                JOIN VALS ON VALCODE_ID = 'INSTITUTION.COHORTS'
                           AND STA_OTHER_COHORT_GROUPS = VALS.VAL_INTERNAL_CODE
                       WHERE VAL_EXTERNAL_REPRESENTATION IN (
                                                             'Cheerleading',
                                                             'Dance',
                                                             'Football',
                                                             'Indoor Men''s Track',
                                                             'Indoor Women''s Track',
                                                             'Men''s Basketball',
                                                             'Men''s Basketball - JV',
                                                             'Men''s Cross Country',
                                                             'Men''s Golf',
                                                             'Men''s Soccer',
                                                             'Men''s Soccer - JV',
                                                             'Outdoor Men''s Track',
                                                             'Outdoor Women''s Track',
                                                             'Women''s Basketball',
                                                             'Women''s Basketball - JV',
                                                             'Women''s Cross Country',
                                                             'Women''s Golf',
                                                             'Women''s Soccer',
                                                             'Women''s  Softball',
                                                             'Women''s Volleyball',
                                                             'Women''s Volleyball - JV'
                           )
                         AND STA_STUDENT = COHORT.ID
                       AND STA_OTHER_COHORT_START_DATES < DATEADD(YEAR, 6, START_TERM.TERM_START_DATE))
         AND PERSON.GENDER = 'M'
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY School, Year
--(End 2)---------------------------------------------------------------------------------------------------------------