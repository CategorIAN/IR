
--(Begin 2)------------------------------------------------------------------------------------------------------------
SELECT LOAD AS LOAD_OF_LAST_TERM,
       COUNT(*) AS GRADUATED_STUDENTS_IN_2024SP_OR_2024SU
FROM (
--(Begin 1)------------------------------------------------------------------------------------------------------------
         SELECT PERSON.ID,
                CASE
                    WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                    ELSE 'Part-Time' END AS LOAD
         FROM Z01_PERSON AS PERSON
                  JOIN SPT_STUDENT_PROGRAMS AS SP ON PERSON.ID = SP.STPR_STUDENT
                  JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
                  JOIN ODS_STUDENT_TERMS ON PERSON.ID = ODS_STUDENT_TERMS.STTR_STUDENT
                  LEFT JOIN ODS_TERMS ON STTR_TERM = TERMS_ID
         WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND STTR_TERM IN ('2024SP', '2024SU')
           AND SP.CURRENT_STATUS_DESC = 'Graduated'
           AND SP.END_DATE BETWEEN TERM_START_DATE AND DATEADD(WEEK, 1, TERM_END_DATE)
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY LOAD
--(End 2)---------------------------------------------------------------------------------------------------------------