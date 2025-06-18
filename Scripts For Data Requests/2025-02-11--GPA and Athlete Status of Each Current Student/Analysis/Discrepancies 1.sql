--(Begin 2)--------------------------------------------------------------------------------
SELECT SUM(TERM_GPA_2024FA) AS SUM
FROM (
--(Begin 1)--------------------------------------------------------------------------------
         SELECT ID,
                STUDENT_TERM_GPA AS TERM_GPA_2024FA
         FROM [PERSON]
                  JOIN [STUDENT_TERM_GPA_VIEW] ON PERSON.ID = STUDENT_TERM_GPA_VIEW.STUDENT_ID
         WHERE STUDENT_TERM_GPA_VIEW.TERM = '2024FA'
--(End 1)----------------------------------------------------------------------------------
     ) AS X
--(End 2)----------------------------------------------------------------------------------


--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


--(Begin 3)--------------------------------------------------------------------------------
SELECT SUM(TERM_GPA) AS SUM
FROM (
--(Begin 2)--------------------------------------------------------------------------------
         SELECT ID,
                SUM(STC_CUM_CONTRIB_GRADE_PTS) / SUM(STC_CUM_CONTRIB_CMPL_CRED) AS TERM_GPA
         FROM (
--(Begin 1)--------------------------------------------------------------------------------
                  SELECT ID,
                         STC_CUM_CONTRIB_CMPL_CRED,
                         STC_CUM_CONTRIB_GRADE_PTS
                  FROM [PERSON]
                           JOIN STUDENT_ACAD_CRED ON PERSON.ID = STUDENT_ACAD_CRED.STC_PERSON_ID
                  WHERE STUDENT_ACAD_CRED.STC_TERM = '2024FA'
                    AND STC_CRED_TYPE = 'INST'
                    AND STC_CUM_CONTRIB_CMPL_CRED > 0
--(End 1)----------------------------------------------------------------------------------
              ) AS X
         GROUP BY ID
--(End 2)----------------------------------------------------------------------------------
     ) AS X
--(End 3)----------------------------------------------------------------------------------


--~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--(Begin 3)--------------------------------------------------------------------------------
SELECT *
FROM (
--(Begin 2)--------------------------------------------------------------------------------
         SELECT ID,
                STUDENT_TERM_GPA                                      AS TERM_GPA_1,
                SUM(STC_CUM_CONTRIB_GRADE_PTS) / SUM(STC_CUM_CONTRIB_CMPL_CRED) AS TERM_GPA_2
         FROM (
--(Begin 1)--------------------------------------------------------------------------------
                  SELECT ID,
                         STC_CUM_CONTRIB_CMPL_CRED,
                         STC_CUM_CONTRIB_GRADE_PTS
                  FROM [PERSON]
                           JOIN STUDENT_ACAD_CRED ON PERSON.ID = STUDENT_ACAD_CRED.STC_PERSON_ID
                  WHERE STUDENT_ACAD_CRED.STC_TERM = '2024FA'
                    AND STC_CRED_TYPE = 'INST'
                    AND STC_CUM_CONTRIB_CMPL_CRED > 0
--(End 1)----------------------------------------------------------------------------------
              ) AS X
                  JOIN STUDENT_TERM_GPA_VIEW ON X.ID = STUDENT_ID
         GROUP BY ID, STUDENT_TERM_GPA
--(End 2)----------------------------------------------------------------------------------
     ) AS X
WHERE TERM_GPA_1 != TERM_GPA_2
--(End 3)----------------------------------------------------------------------------------








