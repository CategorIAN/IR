--(Begin 1)-------------------------------------------------------------------------------------------------------------
 SELECT DISTINCT STPR_STUDENT,
                PERSON.FIRST_NAME,
                PERSON.LAST_NAME,
                CASE WHEN EXISTS (
                    SELECT 1
                    FROM ODS_STUDENT_TERMS AS Y
                    WHERE Y.STTR_STUDENT = STPR_STUDENT
                    AND STTR_TERM IN ('2024FA', '2025SP', '2025SU')
                ) THEN 1 ELSE 0 END AS IN_2024FA_2025SP_OR_2025SU
 FROM SPT_STUDENT_PROGRAMS AS SP
          JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
          JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
 WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
   AND SP.START_DATE <= '2024-07-01'
   AND COALESCE(SP.END_DATE, GETDATE()) >= '2024-07-01'
   AND CURRENT_STATUS_DESC != 'Did Not Enroll'
   AND (CURRENT_STATUS_DESC NOT IN ('Not Returned', 'Changed Program') OR CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)---------------------------------------------------------------------------------------------------------------
ORDER BY LAST_NAME, FIRST_NAME