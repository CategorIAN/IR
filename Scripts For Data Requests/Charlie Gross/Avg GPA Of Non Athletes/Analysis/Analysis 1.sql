SELECT ID,
       STUDENT_OVERALL_CUM_GPA,
       STUDENT_TERM_GPA,
       COUNT(*) AS COUNT
FROM (SELECT PERSON.ID,
             STUDENT_OVERALL_CUM_GPA,
             STUDENT_TERM_GPA
      FROM [PERSON]
               JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
               JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
               Left JOIN [STA_OTHER_COHORTS_VIEW] ON PERSON.ID = STA_OTHER_COHORTS_VIEW.STA_STUDENT
      WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA'
        and (
          STA_OTHER_COHORT_GROUPS IN
          ('HNRS', 'FOR', 'ROTC', 'VETS', 'INTL', 'ACCESS', 'CIC', 'GRSET', 'GRSUA', 'GRSMX') OR
          STA_OTHER_COHORT_GROUPS IS NULL OR
          STA_OTHER_COHORT_END_DATES < GETDATE()
          )) AS X
GROUP BY ID, STUDENT_OVERALL_CUM_GPA, STUDENT_TERM_GPA
HAVING COUNT(*) > 1

------------------------------------------------------------------------------------------------------------------------
--(Begin 2)--------------------------------------------------------------------------------------------
SELECT
       AVG(STUDENT_OVERALL_CUM_GPA)  AS AVG_CUMULATIVE_GPA,
       AVG(STUDENT_TERM_GPA)  AS AVG_TERM_GPA_2024FA
FROM (
--(Begin 1)--------------------------------------------------------------------------------------------
SELECT       DISTINCT PERSON.ID,
             STUDENT_OVERALL_CUM_GPA,
             STUDENT_TERM_GPA
      FROM [PERSON]
       JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
       JOIN (SELECT STUDENT_ID,
                    STUDENT_TERM_GPA
             FROM [STUDENT_TERM_GPA_VIEW]
             WHERE TERM = '2024FA') AS X ON PERSON.ID = X.STUDENT_ID
       WHERE NOT EXISTS (
        SELECT 1
        FROM STA_OTHER_COHORTS_VIEW
        WHERE
          STA_OTHER_COHORT_GROUPS IN (
                                      'BBM',
                                      'BBMJV',
                                      'BBW',
                                      'BBWJV',
                                      'CHER',
                                      'DANCE',
                                      'DNCE',
                                      'FTBL',
                                      'GOLM',
                                      'GOLW',
                                      'ITRKM',
                                      'ITRKW',
                                      'OTRKM',
                                      'OTRKW',
                                      'SOFBW',
                                      'SOM',
                                      'SOMJV',
                                      'SOW',
                                      'VBW',
                                      'VBWJV',
                                      'XCM',
                                      'XCW'
              )
         AND (STA_OTHER_COHORT_END_DATES >= GETDATE() OR STA_OTHER_COHORT_END_DATES IS NULL)
        AND STA_STUDENT = PERSON.ID
          )
--(End 1)----------------------------------------------------------------------------------------------
) AS X
--(End 2)----------------------------------------------------------------------------------------------




--(Begin 2)--------------------------------------------------------------------------------------------
SELECT
       AVG(STUDENT_OVERALL_CUM_GPA)  AS AVG_CUMULATIVE_GPA,
       AVG(STUDENT_TERM_GPA)  AS AVG_TERM_GPA_2024FA
FROM (
--(Begin 1)--------------------------------------------------------------------------------------------
SELECT       DISTINCT PERSON.ID,
             STUDENT_OVERALL_CUM_GPA,
             STUDENT_TERM_GPA
      FROM [PERSON]
       JOIN [STUDENT_CUM_GPA_VIEW_DETAIL] ON PERSON.ID = STUDENT_CUM_GPA_VIEW_DETAIL.STUDENT_ID
      JOIN (SELECT STUDENT_ID,
                STUDENT_TERM_GPA
         FROM [STUDENT_TERM_GPA_VIEW]
         WHERE TERM = '2024FA') AS X ON PERSON.ID = X.STUDENT_ID
        WHERE NOT EXISTS (
        SELECT 1
        FROM STA_OTHER_COHORTS_VIEW
        WHERE
          STA_OTHER_COHORT_GROUPS IN (
                                      'BBM',
                                      'BBMJV',
                                      'BBW',
                                      'BBWJV',
                                      'CHER',
                                      'DANCE',
                                      'DNCE',
                                      'FTBL',
                                      'GOLM',
                                      'GOLW',
                                      'ITRKM',
                                      'ITRKW',
                                      'OTRKM',
                                      'OTRKW',
                                      'SOFBW',
                                      'SOM',
                                      'SOMJV',
                                      'SOW',
                                      'VBW',
                                      'VBWJV',
                                      'XCM',
                                      'XCW'
              )
         AND (STA_OTHER_COHORT_END_DATES >= GETDATE() OR STA_OTHER_COHORT_END_DATES IS NULL)
        AND STA_STUDENT = PERSON.ID
          )
--(End 1)----------------------------------------------------------------------------------------------
) AS X
--(End 2)----------------------------------------------------------------------------------------------



--(Begin 2)--------------------------------------------------------------------------------------------
SELECT ID,
       CUM_GPA_1,
       CUM_GPA_2
FROM (
--(Begin 1)--------------------------------------------------------------------------------------------
         SELECT DISTINCT PERSON.ID,
                         STUDENT_CUM_GPA_VIEW.STUDENT_OVERALL_CUM_GPA        AS CUM_GPA_1,
                         STUDENT_CUM_GPA_VIEW_DETAIL.STUDENT_OVERALL_CUM_GPA AS CUM_GPA_2,
                         STUDENT_TERM_GPA
         FROM [PERSON]
                  LEFT JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
                  LEFT JOIN [STUDENT_CUM_GPA_VIEW_DETAIL] ON PERSON.ID = STUDENT_CUM_GPA_VIEW_DETAIL.STUDENT_ID
                  JOIN (SELECT STUDENT_ID,
                               STUDENT_TERM_GPA
                        FROM [STUDENT_TERM_GPA_VIEW]
                        WHERE TERM = '2024FA') AS X ON PERSON.ID = X.STUDENT_ID
         WHERE NOT EXISTS (SELECT 1
                           FROM STA_OTHER_COHORTS_VIEW
                           WHERE STA_OTHER_COHORT_GROUPS IN (
                                                             'BBM',
                                                             'BBMJV',
                                                             'BBW',
                                                             'BBWJV',
                                                             'CHER',
                                                             'DANCE',
                                                             'DNCE',
                                                             'FTBL',
                                                             'GOLM',
                                                             'GOLW',
                                                             'ITRKM',
                                                             'ITRKW',
                                                             'OTRKM',
                                                             'OTRKW',
                                                             'SOFBW',
                                                             'SOM',
                                                             'SOMJV',
                                                             'SOW',
                                                             'VBW',
                                                             'VBWJV',
                                                             'XCM',
                                                             'XCW'
                               )
                             AND (STA_OTHER_COHORT_END_DATES >= GETDATE() OR STA_OTHER_COHORT_END_DATES IS NULL)
                             AND STA_STUDENT = PERSON.ID)
--(End 1)----------------------------------------------------------------------------------------------
     ) AS X
WHERE (CUM_GPA_1 IS NULL AND CUM_GPA_2 IS NOT NULL)
OR (CUM_GPA_1 IS NOT NULL AND CUM_GPA_2 IS NULL)
OR CUM_GPA_1 != CUM_GPA_2
--(End 2)----------------------------------------------------------------------------------------------
