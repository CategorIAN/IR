--(Begin 4)--------------------------------------------------------------------------------------------
SELECT
       AVG(CUM_GPA)  AS AVG_CUMULATIVE_GPA
FROM (
--(Begin 3)--------------------------------------------------------------------------------------------
         SELECT ID,
                TOTAL_GRADE_PTS / TOTAL_CMPL_CRED AS CUM_GPA
         FROM (
--(Begin 2)--------------------------------------------------------------------------------------------
                  SELECT ID,
                         SUM(STC_CUM_CONTRIB_GRADE_PTS) AS TOTAL_GRADE_PTS,
                         SUM(STC_CUM_CONTRIB_CMPL_CRED) AS TOTAL_CMPL_CRED
                  FROM (
--(Begin 1)--------------------------------------------------------------------------------------------
                           SELECT PERSON.ID,
                                  STC_CUM_CONTRIB_CMPL_CRED,
                                  STC_CUM_CONTRIB_GRADE_PTS
                           FROM [PERSON]
                                    JOIN STUDENT_ACAD_CRED ON PERSON.ID = STUDENT_ACAD_CRED.STC_PERSON_ID
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
                                               AND (STA_OTHER_COHORT_END_DATES >= GETDATE() OR
                                                    STA_OTHER_COHORT_END_DATES IS NULL)
                                               AND STA_STUDENT = PERSON.ID)
                             AND STC_CRED_TYPE = 'INST'
                             AND STC_ACAD_LEVEL = 'UG'
--(End 1)----------------------------------------------------------------------------------------------
                       ) AS X
                  GROUP BY ID
--(End 2)----------------------------------------------------------------------------------------------
              ) AS X
         WHERE TOTAL_CMPL_CRED > 0
--(End 3)----------------------------------------------------------------------------------------------
     ) AS X
--(End 4)----------------------------------------------------------------------------------------------



--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--(Begin 2)--------------------------------------------------------------------------------------------
SELECT
       AVG(STUDENT_OVERALL_CUM_GPA)  AS AVG_CUMULATIVE_GPA
FROM (
--(Begin 1)--------------------------------------------------------------------------------------------
SELECT       DISTINCT PERSON.ID,
             STUDENT_OVERALL_CUM_GPA
      FROM [PERSON]
       JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
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
       AND TRANSCRIPT_GROUPINGS_ID = 'UG'
--(End 1)----------------------------------------------------------------------------------------------
) AS X
--(End 2)----------------------------------------------------------------------------------------------


--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--(Begin 4)--------------------------------------------------------------------------------------------
         SELECT X.ID,
                X.CUM_GPA                                    AS CUM_GPA_1,
                STUDENT_CUM_GPA_VIEW.STUDENT_OVERALL_CUM_GPA AS CUM_GPA_2
         FROM (
--(Begin 3)--------------------------------------------------------------------------------------------
                  SELECT ID,
                         TOTAL_GRADE_PTS / TOTAL_CMPL_CRED AS CUM_GPA
                  FROM (
--(Begin 2)--------------------------------------------------------------------------------------------
                           SELECT ID,
                                  SUM(STC_CUM_CONTRIB_GRADE_PTS) AS TOTAL_GRADE_PTS,
                                  SUM(STC_CUM_CONTRIB_CMPL_CRED) AS TOTAL_CMPL_CRED
                           FROM (
--(Begin 1)--------------------------------------------------------------------------------------------
                                    SELECT PERSON.ID,
                                           STC_CUM_CONTRIB_CMPL_CRED,
                                           STC_CUM_CONTRIB_GRADE_PTS
                                    FROM [PERSON]
                                             JOIN STUDENT_ACAD_CRED ON PERSON.ID = STUDENT_ACAD_CRED.STC_PERSON_ID
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
                                                        AND (STA_OTHER_COHORT_END_DATES >= GETDATE() OR
                                                             STA_OTHER_COHORT_END_DATES IS NULL)
                                                        AND STA_STUDENT = PERSON.ID)
                                      AND STC_CRED_TYPE = 'INST'
                                      AND STC_ACAD_LEVEL = 'UG'
--(End 1)----------------------------------------------------------------------------------------------
                                ) AS X
                           GROUP BY ID
--(End 2)----------------------------------------------------------------------------------------------
                       ) AS X
                  WHERE TOTAL_CMPL_CRED > 0
--(End 3)----------------------------------------------------------------------------------------------
              ) AS X
                  JOIN STUDENT_CUM_GPA_VIEW ON X.ID = STUDENT_ID
         WHERE TRANSCRIPT_GROUPINGS_ID = 'UG'
--(End 4)----------------------------------------------------------------------------------------------



