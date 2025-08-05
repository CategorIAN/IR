--(Begin 3)------------------------------------------------------------------------------------------
SELECT LOAD,
       GRADUATED_IN_2024FA,
       COUNT(*) AS STUDENT_COUNT
FROM (
--(Begin 2)------------------------------------------------------------------------------------------
         SELECT STUDENT_ID,
                LOAD,
                GRADUATED_IN_2024FA
         FROM (
--(Begin 1)------------------------------------------------------------------------------------------
                  SELECT DISTINCT STUDENT_ID,
                                  CASE WHEN
                                      (STP_CURRENT_STATUS = 'Graduated'
                                        AND STP_END_DATE BETWEEN '2024-08-21' AND '2025-01-01')
                                      THEN 'Yes' ELSE 'No' END AS GRADUATED_IN_2024FA,
                                  CASE WHEN STV.STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY CASE
                                                                                          WHEN STTR_STUDENT_LOAD IN ('F', 'O')
                                                                                              THEN 1
                                                                                          ELSE 0 END)         AS LOAD_RANK
                  FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                           JOIN PERSON ON SAPV.STUDENT_ID = PERSON.ID
                  JOIN STUDENT_TERMS_VIEW AS STV ON SAPV.STUDENT_ID = STV.STTR_STUDENT
                  WHERE STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
                    AND STP_START_DATE <= '2024-07-01'
                    AND COALESCE(STP_END_DATE, GETDATE()) >= '2024-07-01'
                    AND STP_CURRENT_STATUS != 'Did Not Enroll'
                    AND (STP_CURRENT_STATUS NOT IN ('Not Returned', 'Changed Program') OR
                         STP_CURRENT_STATUS_DATE > '2024-07-01')
                    AND STTR_TERM IN ('2024FA', '2025SP', '2025SU')
--(End 1)--------------------------------------------------------------------------------------------
              ) AS X
         WHERE LOAD_RANK = 1
--(End 2)--------------------------------------------------------------------------------------------
     ) AS X
GROUP BY LOAD, GRADUATED_IN_2024FA
--(End 3)--------------------------------------------------------------------------------------------


