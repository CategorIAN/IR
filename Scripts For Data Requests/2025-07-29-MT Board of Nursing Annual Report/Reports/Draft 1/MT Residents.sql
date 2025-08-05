--(Begin 2)------------------------------------------------------------------------------------------
SELECT FORMAT(AVG(CAST(CASE WHEN STATE = 'MT' THEN 1 ELSE 0 END AS FLOAT)), 'P') AS MT_RESIDENT_AVERAGE
FROM (
--(Begin 1)------------------------------------------------------------------------------------------
         SELECT STUDENT_ID,
                PAV.STATE,
                ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY
                    CASE WHEN ADDRESS_TYPE = 'H' THEN 0 ELSE 1 END, ADDRESS_ADD_DATE) AS ADDRESS_RANK
         FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  JOIN PERSON ON SAPV.STUDENT_ID = PERSON.ID
                  JOIN PERSON_ADDRESSES_VIEW AS PAV ON SAPV.STUDENT_ID = PAV.ID
                  JOIN ADDRESS ON PAV.ADDRESS_ID = ADDRESS.ADDRESS_ID
         WHERE STP_PROGRAM_TITLE IN ('Nursing', 'Accelerated Nursing')
           AND STP_START_DATE <= '2024-07-01'
           AND COALESCE(STP_END_DATE, GETDATE()) >= '2024-07-01'
           AND STP_CURRENT_STATUS != 'Did Not Enroll'
            AND (STP_CURRENT_STATUS NOT IN ('Not Returned', 'Changed Program') OR STP_CURRENT_STATUS_DATE > '2024-07-01')
--(End 1)--------------------------------------------------------------------------------------------
     ) AS X
WHERE ADDRESS_RANK = 1
--(End 2)--------------------------------------------------------------------------------------------