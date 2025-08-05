--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(CAST(CASE WHEN STATE = 'MT' THEN 1 ELSE 0 END AS FLOAT)), 'P') AS MT_RESIDENT_AVERAGE
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT STPR_STUDENT                                                           AS ID,
                         STATE,
                         ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT ORDER BY
                             CASE WHEN ADDR_TYPE = 'H' THEN 0 ELSE 1 END, ADDR_EFFECTIVE_START) AS ADDRESS_RANK
         FROM SPT_STUDENT_PROGRAMS AS SP
                  JOIN SPT_ACAD_PROGRAMS AS AP ON SP.STPR_ACAD_PROGRAM = AP.ACAD_PROGRAMS_ID
                  JOIN Z01_PERSON PERSON ON SP.STPR_STUDENT = PERSON.ID
                  JOIN SPT_PERSON_ADDRESS_INFO AS PA ON SP.STPR_STUDENT = PA.ID
                  JOIN ODS_ADDRESS ON PA.PERSON_ADDRESSES = ADDRESS_ID
         WHERE ACPG_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND SP.START_DATE <= '2024-07-01'
           AND COALESCE(SP.END_DATE, GETDATE()) >= '2024-07-01'
           AND CURRENT_STATUS_DESC != 'Did Not Enroll'
           AND (CURRENT_STATUS_DESC NOT IN ('Not Returned', 'Changed Program') OR CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)---------------------------------------------------------------------------------------------------------------
     ) AS X
WHERE ADDRESS_RANK = 1
--(End 2)---------------------------------------------------------------------------------------------------------------
