--(Begin 2)------------------------------------------------------------------------------------------------------
SELECT ID,
       LAST_NAME,
       FIRST_NAME,
       COUNT(*) AS COUNT
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------
            SELECT ID,
             LAST_NAME,
             FIRST_NAME,
             STUDENT_OVERALL_CUM_GPA AS CUMULATIVE_GPA,
             STUDENT_TERM_GPA        AS TERM_GPA_2024FA,
             CASE
                 WHEN
                     EXISTS (SELECT 1
                             FROM [STA_OTHER_COHORTS_VIEW]
                             WHERE STA_STUDENT = ID
                               AND STA_OTHER_COHORT_GROUPS IN (
                                                               'FTBL', 'SOW', 'XCW', 'OTRKM', 'ITRKM',
                                                               'XCM', 'GOLW', 'BBM', 'CHER', 'GOLM',
                                                               'VBW', 'BBW', 'ITRKW', 'OTRKW', 'SOFBW',
                                                               'SOM', 'VBWJV', 'BBWJV', 'SOMJV', 'BBMJV',
                                                               'DNCE')
                               and (STA_OTHER_COHORT_END_DATES is NULL or STA_OTHER_COHORT_END_DATES > GETDATE()))
                     THEN 'Athlete'
                 ELSE 'Non-Athlete'
                 END                 AS Athlete_Status
      FROM [PERSON]
               JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
               JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
      WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA'
      GROUP BY ID, LAST_NAME, FIRST_NAME, STUDENT_OVERALL_CUM_GPA, STUDENT_TERM_GPA
--(End 1)---------------------------------------------------------------------------------------------------------------
    ) AS X
GROUP BY ID,
       LAST_NAME,
       FIRST_NAME
HAVING COUNT(*) > 1
--(End 2)---------------------------------------------------------------------------------------------------------------


--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--(Begin 1)------------------------------------------------------------------------------------------------------
            SELECT ID,
             LAST_NAME,
             FIRST_NAME,
             STUDENT_OVERALL_CUM_GPA AS CUMULATIVE_GPA,
             STUDENT_TERM_GPA        AS TERM_GPA_2024FA,
             CASE
                 WHEN
                     EXISTS (SELECT 1
                             FROM [STA_OTHER_COHORTS_VIEW]
                             WHERE STA_STUDENT = ID
                               AND STA_OTHER_COHORT_GROUPS IN (
                                                               'FTBL', 'SOW', 'XCW', 'OTRKM', 'ITRKM',
                                                               'XCM', 'GOLW', 'BBM', 'CHER', 'GOLM',
                                                               'VBW', 'BBW', 'ITRKW', 'OTRKW', 'SOFBW',
                                                               'SOM', 'VBWJV', 'BBWJV', 'SOMJV', 'BBMJV',
                                                               'DNCE')
                               and (STA_OTHER_COHORT_END_DATES is NULL or STA_OTHER_COHORT_END_DATES > GETDATE()))
                     THEN 'Athlete'
                 ELSE 'Non-Athlete'
                 END                 AS Athlete_Status
      FROM [PERSON]
               JOIN [STUDENT_CUM_GPA_VIEW] ON PERSON.ID = STUDENT_CUM_GPA_VIEW.STUDENT_ID
               JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
      WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA'
      AND ID = '6079194'
      GROUP BY ID, LAST_NAME, FIRST_NAME, STUDENT_OVERALL_CUM_GPA, STUDENT_TERM_GPA
--(End 1)---------------------------------------------------------------------------------------------------------------
