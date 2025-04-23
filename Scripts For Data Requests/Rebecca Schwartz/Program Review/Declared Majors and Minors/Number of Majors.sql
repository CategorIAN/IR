--(Begin 2)-------------------------------------------------------------------------------------------------------------
SELECT MAJOR,
       [2021],
       [2022],
       [2023],
       [2024],
       [2025]
FROM (
--(Begin 1)-------------------------------------------------------------------------------------------------------------
         SELECT DISTINCT YEAR_ID         AS YEAR,
                         MAJORS.MAJ_DESC AS MAJOR,
                         STUDENT_ID
         FROM MAJORS
                  CROSS JOIN (VALUES ('2025', CAST('2025-01-01 00:00:00' AS DATETIME)),
                                     ('2024', CAST('2024-01-01 00:00:00' AS DATETIME)),
                                     ('2023', CAST('2023-01-01 00:00:00' AS DATETIME)),
                                     ('2022', CAST('2022-01-01 00:00:00' AS DATETIME)),
                                     ('2021', CAST('2021-01-01 00:00:00' AS DATETIME))) AS YEARS(YEAR_ID, START)
                  CROSS JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                  LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                            ON SAPV.STUDENT_ID = STPR_STUDENT AND STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                  LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                  LEFT JOIN MAJORS AS ADDNL_MAJOR ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
         WHERE STP_START_DATE < DATEADD(YEAR, 1, START)
           AND (STP_END_DATE >= START OR STP_END_DATE IS NULL)
           AND (
             (MAJORS.MAJORS_ID = MAIN_MAJOR.MAJORS_ID)
                 OR (MAJORS.MAJORS_ID = ADDNL_MAJOR.MAJORS_ID
                 AND STPR_ADDNL_MAJOR_START_DATE < DATEADD(YEAR, 1, START)
                 AND (STPR_ADDNL_MAJOR_END_DATE >= START OR STPR_ADDNL_MAJOR_END_DATE IS NULL)
                 )
             )
--(End 1)-------------------------------------------------------------------------------------------------------------
     ) AS X
PIVOT (COUNT(STUDENT_ID) FOR YEAR IN ([2021],
                                       [2022],
                                       [2023],
                                       [2024],
                                       [2025])) AS X
--(End 2)-------------------------------------------------------------------------------------------------------------
