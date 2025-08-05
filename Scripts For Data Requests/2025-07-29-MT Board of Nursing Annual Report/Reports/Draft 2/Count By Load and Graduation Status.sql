--(Begin 3)-------------------------------------------------------------------------------------------------------------
SELECT LOAD,
       GRADUATED_IN_2024FA,
       COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT ID,
                LOAD,
                GRADUATED_IN_2024FA
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
                  SELECT DISTINCT STPR_STUDENT                                                                    AS ID,
                                  CASE
                                      WHEN (CURRENT_STATUS_DESC = 'Graduated'
                                          AND END_DATE BETWEEN '2024-08-21' AND '2025-01-01') THEN 'Yes'
                                      ELSE 'No'
                                      END                                                                         AS GRADUATED_IN_2024FA,
                                  CASE
                                      WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                                      ELSE 'Part-Time' END                                                        AS LOAD,
                                  ROW_NUMBER() OVER
                                      (PARTITION BY STPR_STUDENT ORDER BY CASE WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 1 ELSE 0 END)
                                                                                                                  AS LOAD_RANK
                  FROM SPT_STUDENT_PROGRAMS AS SP
                           JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
                           JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
                           JOIN ODS_STUDENT_TERMS ON SP.STPR_STUDENT = STTR_STUDENT
                  WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
                    AND SP.START_DATE <= '2024-07-01'
                    AND COALESCE(SP.END_DATE, GETDATE()) >= '2024-07-01'
                    AND CURRENT_STATUS_DESC != 'Did Not Enroll'
                    AND (CURRENT_STATUS_DESC NOT IN ('Not Returned', 'Changed Program') OR
                         CURRENT_STATUS_DATE > '2024-07-01')
                    AND STTR_TERM IN ('2024FA', '2025SP', '2025SU')
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         WHERE LOAD_RANK = 1
--(End 2)---------------------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY LOAD, GRADUATED_IN_2024FA
--(End 3)---------------------------------------------------------------------------------------------------------------

