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
                    AND (TERMS.TERMS_ID LIKE '%FA')
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
ORDER BY TERM_START_DATE



SELECT X.*,
       FM.TERM
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
                    AND (TERMS.TERMS_ID LIKE '%FA')
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
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON X.STUDENT_ID = FM.ID


