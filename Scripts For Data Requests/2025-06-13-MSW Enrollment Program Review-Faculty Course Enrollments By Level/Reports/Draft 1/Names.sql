--(Begin 1)--------------------------------------------------------------------------------------
         SELECT STUDENTS.*,
                SEV.SECTION_COURSE_NAME          AS COURSE_NAME,
                SEV.SECTION_COURSE_TITLE         AS COURSE_TITLE,
                COURSE_SECTIONS.SEC_FACULTY_INFO AS FACULTY,
                SEV.STUDENT_ACAD_LEVEL AS LEVEL
         FROM (SELECT DISTINCT TERMS.TERMS_ID AS TERM,
                               TERMS.TERM_START_DATE,
                               SAPV.STUDENT_ID,
                               STUDENT_FIRST_NAME,
                               STUDENT_LAST_NAME
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
                 AND (
                   (
                       MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID
                           AND STP_START_DATE <= TERMS.TERM_END_DATE
                           AND (STP_END_DATE >= TERMS.TERM_START_DATE OR STP_END_DATE IS NULL)
                       )
                       OR (
                       MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                           AND STPR_ADDNL_MAJOR_START_DATE <= TERMS.TERM_END_DATE
                           AND
                       (STPR_ADDNL_MAJOR_END_DATE >= TERMS.TERM_START_DATE OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                       )
                   )
                 AND MAJORS.MAJ_DESC = 'Master of Social Work') AS STUDENTS
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STUDENTS.STUDENT_ID = SEV.STUDENT_ID AND TERM = ENROLL_TERM
                  JOIN COURSE_SECTIONS ON SEV.SECTION_COURSE_SECTION_ID = COURSE_SECTIONS_ID
         WHERE ENROLL_CURRENT_STATUS IN ('New', 'Add')
--(End 1)--------------------------------------------------------------------------------------------------------------