--(Begin 1)---------------------------------------------------------------------------------------------------------
         SELECT DISTINCT AC.STC_PERSON_ID AS ID,
                         FIRST_NAME,
                         LAST_NAME,
                         SP.STPR_ACAD_PROGRAM AS PROGRAM,
                         STUDENT_MAJORS_MINORS.MAJOR_OR_MINOR,
                         STUDENT_MAJORS_MINORS.TYPE
         FROM SPT_STUDENT_ACAD_CRED AS AC
             JOIN ODS_PERSON ON AC.STC_PERSON_ID = ODS_PERSON.ID
                  LEFT JOIN SPT_STUDENT_COURSE_SEC AS SEC ON AC.STC_STUDENT_COURSE_SEC = SEC.STUDENT_COURSE_SEC_ID
                  JOIN SPT_STUDENT_PROGRAMS AS SP ON AC.STC_PERSON_ID = SP.STPR_STUDENT
                  JOIN (SELECT STUDENT_PROGRAMS_ID AS ID,
                               MAJOR_DESC         AS MAJOR_OR_MINOR,
                               'Program Major' AS TYPE
                        FROM SPT_STUDENT_PROGRAM_MAJORS
                        WHERE MAJOR_DESC IS NOT NULL
                        UNION
                        SELECT STUDENT_PROGRAMS_ID,
                               ADDNL_MAJOR_DESC,
                               'Additional Major'
                        FROM SPT_STU_PROG_ADDNL_MAJORS
                        WHERE COALESCE(STPR_ADDNL_MAJOR_END_DATE, GETDATE()) >= GETDATE()
                        UNION
                        SELECT STUDENT_PROGRAMS_ID,
                               ADDNL_MINOR_DESC,
                               'Minor'
                        FROM SPT_STU_PROG_ADDNL_MINORS
                        WHERE COALESCE(STPR_MINOR_END_DATE, GETDATE()) >= GETDATE()
                        ) AS STUDENT_MAJORS_MINORS
                       ON SP.STUDENT_PROGRAMS_ID = STUDENT_MAJORS_MINORS.ID
         WHERE AC.CURRENT_STATUS_DESC IN ('New', 'Add')
           AND STC_TERM = '2025FA'
           AND STC_CRED_TYPE = 'INST'
           AND COALESCE(SEC.Z01_SCS_PASS_AUDIT, '') != 'A'
           AND SP.CURRENT_STATUS_DESC = 'Active'
--(End 1)----------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME


SELECT *
FROM SPT_STUDENT_PROGRAM_MAJORS

SELECT *
FROM SPT_STU_PROG_ADDNL_MINORS