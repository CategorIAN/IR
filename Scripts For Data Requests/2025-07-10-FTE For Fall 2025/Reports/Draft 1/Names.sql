--(Begin 1)---------------------------------------------------------------------------------------------
         SELECT STTR_STUDENT,
                LAST_NAME,
                FIRST_NAME,
                CASE
                    WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                    ELSE 'Part-Time' END AS LOAD
         FROM ODS_STUDENT_TERMS
         JOIN Z01_PERSON ON STTR_STUDENT = ID
         WHERE STTR_TERM = '2025FA'
           AND STATUS_DESC = 'Registered'
--(End 1)------------------------------------------------------------------------------------------------
