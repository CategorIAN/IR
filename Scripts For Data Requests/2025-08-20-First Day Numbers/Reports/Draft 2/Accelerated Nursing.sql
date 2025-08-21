--(Begin C1)-------------------------------------------------------------------------------------------------------------
SELECT  TABLE_1.*,
        TABLE_2.PROGRAM,
        TABLE_2.MAJOR_OR_MINOR,
        TABLE_2.TYPE
FROM (
--(Begin A1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STC_PERSON_ID                 AS ID,
                         FIRST_NAME,
                         LAST_NAME,
                         ST.STTR_STUDENT_LOAD          AS LOAD,
                         COALESCE(STT_DESC, 'Unknown') AS STUDENT_TYPE,
                         ACADEMIC_LEVEL_DESC           AS ACADEMIC_LEVEL,
                         STATUS_DESC                   AS TERM_STATUS
         FROM SPT_STUDENT_ACAD_CRED AS STC
                  JOIN ODS_PERSON ON STC.STC_PERSON_ID = ODS_PERSON.ID
                  JOIN ODS_STUDENT_TERMS AS ST
                       ON STC.STC_PERSON_ID + '*' + STC.STC_TERM + '*' + STC.STC_ACAD_LEVEL = STUDENT_TERMS_ID
                  LEFT JOIN (SELECT STUDENTS_ID,
                                    STU_TYPES,
                                    ROW_NUMBER() OVER (PARTITION BY STUDENTS_ID ORDER BY STU_TYPE_DATES DESC) AS RANK
                             FROM Z01_STU_TYPE_INFO) AS Z01_STU_TYPE_INFO ON STC_PERSON_ID = STUDENTS_ID AND RANK = 1
                  LEFT JOIN Z01_STUDENT_TYPES ON Z01_STU_TYPE_INFO.STU_TYPES = Z01_STUDENT_TYPES.STUDENT_TYPES_ID
         WHERE STC_TERM = '2025FA'
           AND STC_CRED_TYPE = 'INST'
--(End A1)---------------------------------------------------------------------------------------------------------------
     ) AS TABLE_1
LEFT JOIN (
--(Begin B1)------------------------------------------------------------------------------------------------------------
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
--(End B1)--------------------------------------------------------------------------------------------------------------
) AS TABLE_2 ON TABLE_1.ID = TABLE_2.ID
WHERE PROGRAM = 'ANUR.BS'
--(End C1)---------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME