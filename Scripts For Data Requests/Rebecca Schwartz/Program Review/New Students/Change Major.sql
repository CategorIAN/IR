--(Begin 5)-------------------------------------------------------------------------------------------------------------
SELECT TERM,
       MAJOR,
       COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 4)------------------------------------------------------------------------------------------------------------
         SELECT TERM,
                TERM_START_DATE,
                MAJOR,
                STUDENT_ID
         FROM (
--(Begin 3)------------------------------------------------------------------------------------------------------------
                  SELECT TERM,
                         TERM_START_DATE,
                         MAJOR,
                         STUDENT_ID,
                         CASE
                             WHEN MAX(CASE WHEN MAJOR_2 = MAJOR THEN 1 ELSE 0 END) = 0 THEN 'Changed Major'
                             ELSE 'Kept Major' END AS MAJOR_CHANGE
                  FROM (
--(Begin 2)------------------------------------------------------------------------------------------------------------
                           SELECT X.TERM,
                                  X.TERM_START_DATE,
                                  X.MAJOR,
                                  X.STUDENT_ID,
                                  Y.MAJOR AS MAJOR_2
                           FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
                                    SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                                                    TERMS.TERM_START_DATE,
                                                    MAJORS.MAJ_DESC AS MAJOR,
                                                    STUDENT_ID
                                    FROM MAJORS
                                             CROSS JOIN TERMS
                                             CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                             LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                       ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                          STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                             LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                             LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                       ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                    WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                                      AND TERMS.TERM_END_DATE < '2025-06-01'
                                      AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                      AND STP_START_DATE <= TERMS.TERM_END_DATE
                                      AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                      AND STP_CURRENT_STATUS != 'Did Not Enroll'
                                      AND (
                                        (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                            OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                            AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                            AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                 STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                            )
                                        )
--(End 1)------------------------------------------------------------------------------------------------------------
                                ) AS X
                                    LEFT JOIN (VALUES ('2019FA', '2020SP'),
                                                      ('2020SP', '2020FA'),
                                                      ('2020FA', '2021SP'),
                                                      ('2021SP', '2021FA'),
                                                      ('2021FA', '2022SP'),
                                                      ('2022SP', '2022FA'),
                                                      ('2022FA', '2023SP'),
                                                      ('2023SP', '2023FA'),
                                                      ('2023FA', '2024SP'),
                                                      ('2024SP', '2024FA'),
                                                      ('2024FA', '2025SP')) AS NEXT_TERM(FIRST, SECOND)
                                              ON X.TERM = NEXT_TERM.FIRST
                                    JOIN (SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                                                          TERMS.TERM_START_DATE,
                                                          MAJORS.MAJ_DESC AS MAJOR,
                                                          STUDENT_ID
                                          FROM MAJORS
                                                   CROSS JOIN TERMS
                                                   CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                                   LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                                             ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                                STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                                   LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                                   LEFT JOIN MAJORS AS ADDNL_MAJOR
                                                             ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                                          WHERE TERMS.TERM_START_DATE >= '2019-08-01'
                                            AND TERMS.TERM_END_DATE < '2025-06-01'
                                            AND (TERMS.TERMS_ID LIKE '%FA' OR TERMS.TERMS_ID LIKE '%SP')
                                            AND STP_START_DATE <= TERMS.TERM_END_DATE
                                            AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                                            AND STP_CURRENT_STATUS != 'Did Not Enroll'
                                            AND (
                                              (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                                                  OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                                                  AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                                                  AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR
                                                       STPR_ADDNL_MAJOR_END_DATE IS NULL)
                                                  )
                                              )) AS Y ON X.STUDENT_ID = Y.STUDENT_ID AND NEXT_TERM.SECOND = Y.TERM
                           WHERE X.MAJOR IN (
                                             'Business: Acctng & Stratg Finc',
                                             'Business: Acctng & Stratg Finc',
                                             'Business: Managmt and Marktng'
                               )
--(End 2)------------------------------------------------------------------------------------------------------------
                       ) AS X
                  GROUP BY TERM, TERM_START_DATE, MAJOR, STUDENT_ID
--(End 3)------------------------------------------------------------------------------------------------------------
              ) AS X
        WHERE MAJOR_CHANGE = 'Changed Major'
--(End 4)------------------------------------------------------------------------------------------------------------
    ) AS X
GROUP BY TERM, TERM_START_DATE, MAJOR
--(End 5)-------------------------------------------------------------------------------------------------------------
ORDER BY TERM_START_DATE
