--(Begin 1)-------------------------------------------------------------------------------------------------------------
 SELECT DISTINCT STPR_STUDENT,
                PERSON.FIRST_NAME,
                PERSON.LAST_NAME
 FROM SPT_STUDENT_PROGRAMS AS SP
          JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
          JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
          JOIN ODS_STUDENT_TERMS ON SP.STPR_STUDENT = STTR_STUDENT
 WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
   AND SP.START_DATE <= '2024-07-01'
   AND COALESCE(SP.END_DATE, GETDATE()) >= '2024-07-01'
   AND CURRENT_STATUS_DESC != 'Did Not Enroll'
   AND (CURRENT_STATUS_DESC NOT IN ('Not Returned', 'Changed Program') OR CURRENT_STATUS_DATE > '2024-07-01')
 AND STTR_TERM IN ('2024FA', '2025SP', '2025SU')
--(End 1)---------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME