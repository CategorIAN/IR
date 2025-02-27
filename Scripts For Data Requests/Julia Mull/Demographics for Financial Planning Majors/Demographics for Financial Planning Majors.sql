SELECT *
FROM (
         (SELECT STUDENT_ID,
                 LAST_NAME,
                 FIRST_NAME,
                 GENDER
          FROM (SELECT STUDENT_ID
                FROM (SELECT * FROM STUDENT_ACAD_PROGRAMS_VIEW
                        WHERE STP_CURRENT_STATUS = 'Active'
                        AND STP_ACAD_LEVEL = 'UG') AS SAPV
                         LEFT JOIN STPR_MAJOR_LIST_VIEW ON SAPV.STUDENT_ID = STPR_MAJOR_LIST_VIEW.STPR_STUDENT AND
                                                           SAPV.STP_ACADEMIC_PROGRAM =
                                                           STPR_MAJOR_LIST_VIEW.STPR_ACAD_PROGRAM
                         LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                         LEFT JOIN MAJORS AS ADDNL_MAJOR
                                   ON STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                WHERE (
                    MAIN_MAJOR.MAJ_DESC = 'Business: Financial Planning'
                        OR (
                        ADDNL_MAJOR.MAJ_DESC = 'Business: Financial Planning'
                            AND STPR_MAJOR_LIST_VIEW.STPR_ADDNL_MAJOR_END_DATE IS NULL
                        )
                    )
                  AND STP_START_DATE < '2025-05-01') AS FP_STUDENTS
                   JOIN PERSON ON FP_STUDENTS.STUDENT_ID = PERSON.ID) AS X
             JOIN (SELECT *
                   FROM Z01_ALL_RACE_ETHNIC_W_FLAGS) AS Y ON X.STUDENT_ID = Y.ID
         )
ORDER BY LAST_NAME, FIRST_NAME