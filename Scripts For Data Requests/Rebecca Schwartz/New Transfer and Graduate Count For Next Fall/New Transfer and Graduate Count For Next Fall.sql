--(Begin 3)-------------------------------------------------------------------------------------------------------------
SELECT SUM(NEW_TRANSFER) AS TOTAL_NEW_TRANSFERS,
       SUM(NEW_GRADUATE) AS TOTAL_NEW_GRADUATES
FROM (
--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT STUDENT,
                CASE WHEN ADMIT = 'TR' THEN 1 ELSE 0 END AS NEW_TRANSFER,
                CASE WHEN LEVEL = 'GR' THEN 1 ELSE 0 END AS NEW_GRADUATE
         FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
                  SELECT STPR_STUDENT                                                                       AS STUDENT,
                         STPR_ACAD_LEVEL                                                                    AS LEVEL,
                         STPR_ADMIT_STATUS                                                                  AS ADMIT,
                         START_DATE,
                         END_DATE,
                         ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT, STPR_ACAD_LEVEL ORDER BY START_DATE) AS PROGRAM_RANK
                  FROM ODS_STUDENT_PROGRAMS AS SP
                  WHERE START_DATE IS NOT NULL
                    AND STPR_ACAD_LEVEL != 'CE'
                    AND TITLE != 'Non-Degree Seeking Students'
--(End 1)-------------------------------------------------------------------------------------------------------------
              ) AS X
                  CROSS JOIN ODS_TERMS
         WHERE PROGRAM_RANK = 1
           AND (ADMIT = 'TR' OR LEVEL = 'GR')
           AND TERMS_ID = '2025FA'
           AND START_DATE >= TERM_START_DATE
           AND START_DATE <= TERM_END_DATE
--(End 2)-------------------------------------------------------------------------------------------------------------
     ) AS X
--(End 3)-------------------------------------------------------------------------------------------------------------

