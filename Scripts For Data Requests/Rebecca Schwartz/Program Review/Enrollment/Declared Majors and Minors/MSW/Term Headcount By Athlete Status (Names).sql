--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT TERMS.TERMS_ID  AS TERM,
                TERMS.TERM_START_DATE,
                MAJORS.MAJ_DESC AS MAJOR,
                STUDENT_ID,
                STUDENT_LAST_NAME,
                STUDENT_FIRST_NAME,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM STA_OTHER_COHORTS_VIEW
                    JOIN (SELECT VAL_INTERNAL_CODE AS CODE, VAL_EXTERNAL_REPRESENTATION AS COHORT
                          FROM VALS
                          WHERE VALCODE_ID = 'INSTITUTION.COHORTS') AS COHORT_CODES
                    ON STA_OTHER_COHORTS_VIEW.STA_OTHER_COHORT_GROUPS = COHORT_CODES.CODE
                    WHERE COHORT IN (
                                        'Cheerleading',
                                        'Dance',
                                        'Football',
                                        'Indoor Men''s Track',
                                        'Indoor Women''s Track',
                                        'Men''s Basketball',
                                        'Men''s Cross Country',
                                        'Men''s Golf',
                                        'Men''s Soccer',
                                        'Outdoor Men''s Track',
                                        'Outdoor Women''s Track',
                                        'Women''s Basketball',
                                        'Women''s Cross Country',
                                        'Women''s Golf',
                                        'Women''s Soccer',
                                        'Women''s Softball',
                                        'Women''s Volleyball'
                                     )
                    AND STA_STUDENT = STUDENT_ID
                    AND (STP_START_DATE <= STA_OTHER_COHORT_END_DATES OR STA_OTHER_COHORT_END_DATES IS NULL)
                    AND (STP_END_DATE >= STA_OTHER_COHORT_START_DATES OR STP_END_DATE IS NULL)
                ) THEN 'Athlete' ELSE 'Not Athlete' END AS ATHLETE_STATUS
         FROM MAJORS
                  CROSS JOIN TERMS
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
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
                 AND (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
           AND MAJORS.MAJ_DESC = 'Master of Social Work'
--(End 1)------------------------------------------------------------------------------------------------------------
ORDER BY TERM_START_DATE, STUDENT_LAST_NAME, STUDENT_FIRST_NAME