--(Begin 2)---------------------------------------------------------------------------------------------
SELECT COALESCE(LOAD, 'FTE') AS LOAD,
       COUNT(*) AS COUNT,
       CAST(SUM(CASE WHEN LOAD = 'Full-Time' THEN 1.0 ELSE 1.0 / 3 END) AS INT) AS WEIGHTED_COUNT
FROM (
--(Begin 1)---------------------------------------------------------------------------------------------
         SELECT STTR_STUDENT,
                CASE
                    WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time'
                    ELSE 'Part-Time' END AS LOAD
         FROM ODS_STUDENT_TERMS
         WHERE STTR_TERM = '2025FA'
           AND STATUS_DESC = 'Registered'
--(End 1)------------------------------------------------------------------------------------------------
     ) AS X
GROUP BY LOAD WITH ROLLUP
--(End 2)------------------------------------------------------------------------------------------------