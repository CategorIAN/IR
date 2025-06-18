--(Begin 7)------------------------------------------------------------------------------------------------------------
SELECT MAJOR,
       MAJOR_COHORT,
       FORMAT(COMPLETION_RATE, 'P') AS COMPLETION_RATE,
       FORMAT(FOUR_YEAR_GRADUATION_RATE, 'P') AS FOUR_YEAR_GRADUATION_RATE,
       FORMAT(SIX_YEAR_GRADUATION_RATE, 'P') AS SIX_YEAR_GRADUATION_RATE,
       STUDENT_COUNT
FROM (
--(Begin 6)------------------------------------------------------------------------------------------------------------
         SELECT MAJOR,
                MAJOR_COHORT,
                AVG(MAJOR_COMPLETED * 1.0)    AS COMPLETION_RATE,
                AVG(FOUR_YEAR_GRADUATE * 1.0) AS FOUR_YEAR_GRADUATION_RATE,
                AVG(SIX_YEAR_GRADUATE * 1.0)  AS SIX_YEAR_GRADUATION_RATE,
                COUNT(*)                      AS STUDENT_COUNT,
                START
         FROM (
--(Begin 5)------------------------------------------------------------------------------------------------------------
                  SELECT MAJOR,
                         STUDENT_ID,
                         MAJOR_COHORT,
                         MAJOR_COMPLETED,
                         CASE
                             WHEN MAJOR_COMPLETED = 1 AND ACAD_END_DATE < DATEADD(YEAR, 4, START) THEN 1
                             ELSE 0 END AS FOUR_YEAR_GRADUATE,
                         CASE
                             WHEN MAJOR_COMPLETED = 1 AND ACAD_END_DATE < DATEADD(YEAR, 4, START) THEN 1
                             ELSE 0 END AS SIX_YEAR_GRADUATE,
                            START
                  FROM (
--(Begin 4)------------------------------------------------------------------------------------------------------------
                           SELECT X.MAJOR,
                                  X.STUDENT_ID,
                                  COHORTS.TERM            AS MAJOR_COHORT,
                                  MAX(COMPLETE)           AS MAJOR_COMPLETED,
                                  COHORTS.TERM_START_DATE AS START,
                                  ACAD_END_DATE
                           FROM (
--(Begin 3)------------------------------------------------------------------------------------------------------------
                                    SELECT MAJOR,
                                           STUDENT_ID,
                                           CASE
                                               WHEN (MAJOR_END >= ACAD_END_DATE OR MAJOR_END IS NULL)
                                                   AND STATUS = 'Graduated' THEN 1
                                               ELSE 0 END AS COMPLETE,
                                           ACAD_END_DATE
                                    FROM (
--(Begin 2)------------------------------------------------------------------------------------------------------------
                                             SELECT MAJOR,
                                                    STUDENT_ID,
                                                    STATUS,
                                                    CASE WHEN MAJOR = MAIN THEN MAIN_END ELSE ADDNL_END END AS MAJOR_END,
                                                    ACAD_END_DATE
                                             FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                                                      SELECT MAJORS.MAJ_DESC           AS MAJOR,
                                                             SAPV.STUDENT_ID,
                                                             STP_CURRENT_STATUS        AS STATUS,
                                                             MAIN_MAJOR.MAJ_DESC       AS MAIN,
                                                             STP_END_DATE              AS MAIN_END,
                                                             STPR_ADDNL_MAJOR_END_DATE AS ADDNL_END,
                                                             AC.ACAD_END_DATE
                                                      FROM MAJORS
                                                               CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                               JOIN ACAD_CREDENTIALS AS AC
                                                                    ON SAPV.STUDENT_ID = AC.ACAD_PERSON_ID AND
                                                                       SAPV.STP_DEGREE = AC.ACAD_DEGREE

                                                               LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                                         ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                            STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                               LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                               LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                                         ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                                      WHERE STP_CURRENT_STATUS != 'Did Not Enroll'
                                                        AND STP_START_DATE >= '2019-08-01'
                                                        AND (
                                                          (
                                                              MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                                              )
                                                              OR (
                                                              MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                              )
                                                          )
                                                        AND MAJORS.MAJ_DESC = 'Master of Social Work'
--(End 1)------------------------------------------------------------------------------------------------------------
                                                  ) AS X
--(End 2)------------------------------------------------------------------------------------------------------------
                                         ) AS X
--(End 3)------------------------------------------------------------------------------------------------------------
                                ) AS X
                                    JOIN (
--(Begin B2)-----------------------------------------------------------------------------------------------------------
                               SELECT MAJOR,
                                      STUDENT_ID,
                                      TERM,
                                      TERM_START_DATE
                               FROM (
--(Begin B1)-----------------------------------------------------------------------------------------------------------
                                        SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                                        TERMS.TERM_START_DATE,
                                                        MAJORS.MAJ_DESC               AS MAJOR,
                                                        SAPV.STUDENT_ID,
                                                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                                            ORDER BY TERM_START_DATE) AS TERM_RANK
                                        FROM MAJORS
                                                 CROSS JOIN TERMS
                                                 CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV

                                                 LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                                           ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                              SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                                 LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                 LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID

                                        WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                                          AND TERMS.TERM_END_DATE < '2025-06-01'
                                          AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                          AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'

                                          AND (
                                            (
                                                MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                                    AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                                    AND
                                                (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                                )
                                                OR (
                                                MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                    AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                                    AND
                                                (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                 SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                )
                                            )
--(End B1)-------------------------------------------------------------------------------------------------------------
                                    ) AS X
                               WHERE TERM_RANK = 1
                                 AND TERM_START_DATE >= '2019-08-01'
--(End B2)-------------------------------------------------------------------------------------------------------------
                           ) AS COHORTS ON X.MAJOR = COHORTS.MAJOR AND X.STUDENT_ID = COHORTS.STUDENT_ID
                           GROUP BY X.MAJOR, X.STUDENT_ID, COHORTS.TERM, COHORTS.TERM_START_DATE, ACAD_END_DATE
--(End 4)------------------------------------------------------------------------------------------------------------
                       ) AS X
--(End 5)------------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY MAJOR, MAJOR_COHORT, START
--(End 6)------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 7)------------------------------------------------------------------------------------------------------------
ORDER BY START, X.COMPLETION_RATE DESC, X.FOUR_YEAR_GRADUATION_RATE DESC, X.SIX_YEAR_GRADUATION_RATE DESC