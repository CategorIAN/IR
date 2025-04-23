--(Begin 3)-------------------------------------------------------------------------------------------------------------
         SELECT X.*,
                SECTION_COURSE_TITLE  AS HONORS_CONVOCATION_MASTER_LIST_COURSE_TITLE,
                ENROLL_GPA_CREDITS    AS HONORS_CONVOCATION_MASTER_LIST_CREDITS,
                ENROLL_VERIFIED_GRADE AS HONORS_CONVOCATION_MASTER_LIST_GRADE_VERIFIED,
                ENROLL_GRADE_POINTS   AS TOTAL_GRADE_POINTS_FOR_COURSE
         FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
                  SELECT STUDENT_ID,
                         NAME_LAST,
                         NAME_FIRST,
                         CLASS_LEVEL_DESC,
                         GPA_FOR_ACAD_LEVEL,
                         CASE
                             WHEN MAX(CASE
                                          WHEN MAIN_MAJOR = 'PUBH' OR (ADDNL_MAJOR = 'PUBH' AND MAJOR_END_DATE IS NULL)
                                              THEN 1
                                          ELSE 0 END) = 1
                                 THEN 'Y' END AS PH,
                         CASE
                             WHEN MAX(CASE
                                          WHEN MAIN_MAJOR = 'HSCI' OR (ADDNL_MAJOR = 'HSCI' AND MAJOR_END_DATE IS NULL)
                                              THEN 1
                                          ELSE 0 END) = 1
                                 THEN 'Y' END AS HS,
                         MAJOR1
                  FROM (
--(Begin 1)----------------------------------------------------------------------------------------------
                           SELECT STUDENT_ID,
                                  STUDENT_LAST_NAME         AS NAME_LAST,
                                  STUDENT_FIRST_NAME        AS NAME_FIRST,
                                  STUDENT_CLASS_LEVEL       AS CLASS_LEVEL_DESC,
                                  STP_EVAL_COMBINED_GPA     AS GPA_FOR_ACAD_LEVEL,
                                  MAIN_MAJOR.MAJORS_ID      AS MAIN_MAJOR,
                                  ADDNL_MAJOR.MAJORS_ID     AS ADDNL_MAJOR,
                                  STPR_ADDNL_MAJOR_END_DATE AS MAJOR_END_DATE,
                                  STP_PROGRAM_TITLE         AS MAJOR1
                           FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                                    LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                              ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                                 STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                                    LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                                    LEFT JOIN MAJORS AS ADDNL_MAJOR
                                              ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                           WHERE STP_PROGRAM_TITLE IN ('Health Sciences', 'Public Health')
                             AND STP_START_DATE <= GETDATE()
                             AND STP_END_DATE IS NULL
                             AND STP_EVAL_COMBINED_GPA >= 3.5
--(End 1)---------------------------------------------------------------------------------------------------------------
                       ) AS X
                  GROUP BY X.STUDENT_ID,
                           NAME_LAST,
                           NAME_FIRST,
                           CLASS_LEVEL_DESC,
                           GPA_FOR_ACAD_LEVEL,
                           MAJOR1
--(End 2)-------------------------------------------------------------------------------------------------------------
              ) AS X
                  JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON X.STUDENT_ID = SEV.STUDENT_ID
         WHERE ENROLL_GPA_CREDITS IS NOT NULL
        AND ENROLL_CREDIT_TYPE = 'Institutional'
--(End 3)-------------------------------------------------------------------------------------------------------------
ORDER BY NAME_FIRST











