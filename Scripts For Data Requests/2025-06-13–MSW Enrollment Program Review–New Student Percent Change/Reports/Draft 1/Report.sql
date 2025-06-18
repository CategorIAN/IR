--(Begin 4)------------------------------------------------------------------------------------------------------------
WITH X AS (
--(Begin 3)------------------------------------------------------------------------------------------------------------
         SELECT TERM,
                COUNT(*) AS MSW_STUDENT_COUNT
         FROM (
--(Begin 2)------------------------------------------------------------------------------------------------------------
                  SELECT TERM,
                         TERM_START_DATE,
                         MAJOR,
                         STUDENT_ID
                  FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                           SELECT DISTINCT TERMS.TERMS_ID                AS TERM,
                                           TERMS.TERM_START_DATE,
                                           MAJORS.MAJ_DESC               AS MAJOR,
                                           SAPV.STUDENT_ID,
                                           ROW_NUMBER() OVER (PARTITION BY STUDENT_ID, MAJORS.MAJ_DESC
                                               ORDER BY TERM_START_DATE) AS TERM_RANK
                           FROM MAJORS
                                    CROSS JOIN TERMS
                                    CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
------------------------------------------------------------------------------------------------------------------------
                                    LEFT JOIN STPR_MAJOR_LIST_VIEW AS SMLV
                                              ON SAPV.STUDENT_ID = SMLV.STPR_STUDENT AND
                                                 SAPV.STP_ACADEMIC_PROGRAM = SMLV.STPR_ACAD_PROGRAM
                                    LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                    LEFT JOIN MAJORS AS ADDNL_MAJOR ON SMLV.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
-----------------------------------------------------------------------------------------------------------------------
                           WHERE TERMS.TERM_START_DATE >= DATEADD(YEAR, -10, '2019-08-01')
                             AND TERMS.TERM_END_DATE < '2025-06-01'
                             AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS_ID LIKE '%SP')
------------------------------------------------------------------------------------------------------------------------
                             AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
------------------------------------------------------------------------------------------------------------------------
                             AND (
                               (
                                   MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                                       AND SAPV.STP_START_DATE <= TERMS.TERM_END_DATE
                                       AND (SAPV.STP_END_DATE >= TERMS.TERM_START_DATE OR SAPV.STP_END_DATE IS NULL)
                                   )
                                   OR (
                                   MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                       AND SMLV.STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                       AND
                                   (SMLV.STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                    SMLV.STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                   )
                               )
------------------------------------------------------------------------------------------------------------------------
                             AND MAJORS.MAJ_DESC = 'Master of Social Work'
--(End 1)------------------------------------------------------------------------------------------------------------
                       ) AS X
                  WHERE TERM_RANK = 1
                    AND TERM_START_DATE >= '2019-08-01'
--(End 2)------------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY TERM, TERM_START_DATE
--(End 3)------------------------------------------------------------------------------------------------------------
     )
    SELECT CONCAT(X.TERM, ' TO ', NEXT_TERM.SECOND) AS TERM_CHANGE,
           X.MSW_STUDENT_COUNT AS FIRST_COUNT,
           Y.MSW_STUDENT_COUNT AS NEXT_TERM_COUNT,
           FORMAT(Y.MSW_STUDENT_COUNT * 1.0 / X.MSW_STUDENT_COUNT - 1, 'P') AS PERCENT_CHANGE
    FROM X LEFT JOIN (VALUES ('2019FA', '2020FA'),
                         ('2020FA', '2021FA'),
                         ('2021FA', '2022FA'),
                         ('2022FA', '2023FA'),
                         ('2023FA', '2024FA')
    ) AS NEXT_TERM(FIRST, SECOND) ON X.TERM = NEXT_TERM.FIRST
    JOIN X AS Y ON NEXT_TERM.SECOND = Y.TERM
--(End 4)------------------------------------------------------------------------------------------------------------