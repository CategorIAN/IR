--(Begin 4)------------------------------------------------------------------------------------------------------------
               SELECT X.*,
                      CAST(ROUND(NUMBER_RETAINED * 1.0 / STUDENT_COUNT, 3) AS FLOAT) AS RETENTION_PERCENTAGE
               FROM (
--(Begin 3)------------------------------------------------------------------------------------------------------------
                        SELECT SPORT,
                               TERM,
                               NEXT_TERM,
                               COUNT(STUDENT) AS STUDENT_COUNT,
                               SUM(RETAINED)  AS NUMBER_RETAINED
                        FROM (
--(Begin 2)------------------------------------------------------------------------------------------------------------
                                 SELECT SPORT,
                                        TERM,
                                        NEXT_TERM,
                                        STUDENT,
                                        CASE WHEN STILL_ENROLLED = 1 OR SINCE_GRADUATED = 1 THEN 1 ELSE 0 END AS RETAINED
                                 FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                                          SELECT VAL_EXTERNAL_REPRESENTATION AS SPORT,
                                                 TERMS_ID                    AS TERM,
                                                 NEXT_TERM.END_TERM          AS NEXT_TERM,
                                                 STA_STUDENT                 AS STUDENT,
                                                 CASE
                                                     WHEN EXISTS (SELECT 1
                                                                  FROM STUDENT_ENROLLMENT_VIEW
                                                                  WHERE ENROLL_TERM = NEXT_TERM.END_TERM
                                                                    AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
                                                                    AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
                                                                    AND STUDENT_ID = STA_STUDENT) THEN 1
                                                     ELSE 0 END              AS STILL_ENROLLED,
                                                 CASE
                                                     WHEN EXISTS (SELECT 1
                                                                  FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                  WHERE STP_CURRENT_STATUS = 'Graduated'
                                                                    AND (
                                                                      STP_END_DATE >= TERMS.TERM_START_DATE
                                                                          OR STP_END_DATE IS NULL
                                                                      )
                                                                    AND STUDENT_ID = STA_STUDENT)
                                                         THEN 1
                                                     ELSE 0 END              AS SINCE_GRADUATED
                                          FROM STA_OTHER_COHORTS_VIEW
                                                   CROSS JOIN (SELECT TERMS_ID, TERM_START_DATE, TERM_END_DATE
                                                               FROM TERMS
                                                               WHERE TERMS_ID IN ('2023FA', '2024FA')) AS TERMS
                                                   JOIN (SELECT VAL_INTERNAL_CODE, VAL_EXTERNAL_REPRESENTATION
                                                         FROM VALS
                                                         WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS SPORTS
                                                        ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS =
                                                           SPORTS.VAL_INTERNAL_CODE
                                                   JOIN (VALUES ('2024FA', '2025SP'), ('2023FA', '2024FA'))
                                              AS NEXT_TERM(START_TERM, END_TERM)
                                                        ON TERMS.TERMS_ID = NEXT_TERM.START_TERM
                                          WHERE STA_OTHER_COHORT_START_DATES <= TERM_END_DATE
                                            AND (
                                              STA_OTHER_COHORT_END_DATES >= TERM_START_DATE
                                                  OR STA_OTHER_COHORT_END_DATES IS NULL
                                              )
                                            AND VAL_EXTERNAL_REPRESENTATION IN (
                                                                                'Men''s Basketball',
                                                                                'Women''s Basketball',
                                                                                'Cheerleading',
                                                                                'Men''s Cross Country',
                                                                                'Women''s Cross Country',
                                                                                'Dance',
                                                                                'Football',
                                                                                'Men''s Golf',
                                                                                'Women''s Golf',
                                                                                'Women''s Soccer',
                                                                                'Men''s Soccer',
                                                                                'Women''s Softball',
                                                                                'Outdoor Women''s Track',
                                                                                'Indoor Women''s Track',
                                                                                'Outdoor Men''s Track',
                                                                                'Indoor Men''s Track',
                                                                                'Women''s Volleyball',
                                                                                'Men''s Basketball'
                                              )
--(End 1)---------------------------------------------------------------------------------------------------------------
                                      ) AS X
--(End 2)---------------------------------------------------------------------------------------------------------------
                             ) AS X
                        GROUP BY SPORT, TERM, NEXT_TERM
--(End 3)---------------------------------------------------------------------------------------------------------------
                    ) AS X
--(End 4)---------------------------------------------------------------------------------------------------------------
ORDER BY SPORT, TERM DESC