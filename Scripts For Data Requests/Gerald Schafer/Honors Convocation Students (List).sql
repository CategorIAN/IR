--(Begin 2)-------------------------------------------------------------------------------------------------------------
         SELECT STUDENT_ID,
                NAME_LAST,
                NAME_FIRST,
                CLASS_LEVEL_DESC,
                PROGRAM_START_DATE,
                CATALOG_YEAR,
                ANTIC_COMPLETION_DATE,
                EVAL_COMB_CRED,
                GPA_FOR_ACAD_LEVEL,
                CASE
                    WHEN MAX(CASE
                                 WHEN MAIN_MAJOR = 'PUBH' OR (ADDNL_MAJOR = 'PUBH' AND MAJOR_END_DATE IS NULL)
                                     THEN 1
                                 ELSE 0 END) = 1
                        THEN 'Y' END AS PH,
                CASE
                    WHEN MAX(CASE
                                 WHEN MAIN_MAJOR = 'HSCI' OR (ADDNL_MAJOR = 'HSCI' AND MAJOR_END_DATE IS NULL)
                                     THEN 1
                                 ELSE 0 END) = 1
                        THEN 'Y' END AS HS,
                MAJOR1,
                (
                SELECT TOP 1 ADDNL_MAJOR.MAJ_DESC AS MAJOR2
                FROM STPR_MAJOR_LIST_VIEW AS MJ
                    LEFT JOIN MAJORS AS ADDNL_MAJOR ON MJ.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                    WHERE MJ.STPR_STUDENT = X.STUDENT_ID
                      AND STPR_ADDNL_MAJOR_END_DATE IS NULL
                    ORDER BY CASE WHEN ADDNL_MAJOR.MAJ_DESC NOT IN ('Public Health', 'Health Sciences') THEN 0 ELSE 1 END
                ) AS MAJOR2
         FROM (
--(Begin 1)----------------------------------------------------------------------------------------------
                  SELECT STUDENT_ID,
                         STUDENT_LAST_NAME            AS NAME_LAST,
                         STUDENT_FIRST_NAME           AS NAME_FIRST,
                         STUDENT_CLASS_LEVEL          AS CLASS_LEVEL_DESC,
                         CAST(STP_START_DATE AS DATE)        AS PROGRAM_START_DATE,
                         STP_CATALOG                   AS CATALOG_YEAR,
                         STP_ANT_CMPL_DATE              AS ANTIC_COMPLETION_DATE,
                         STP_EVAL_COMBINED_CREDITS      AS EVAL_COMB_CRED,
                         STP_EVAL_COMBINED_GPA        AS GPA_FOR_ACAD_LEVEL,
                         MAIN_MAJOR.MAJORS_ID         AS MAIN_MAJOR,
                         ADDNL_MAJOR.MAJORS_ID        AS ADDNL_MAJOR,
                         STPR_ADDNL_MAJOR_END_DATE    AS MAJOR_END_DATE,
                         MAIN_MAJOR.MAJ_DESC          AS MAJOR1
                  FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                           LEFT JOIN STPR_MAJOR_LIST_VIEW AS STUDENT_MAJORS
                                     ON SAPV.STUDENT_ID = STPR_STUDENT AND
                                        STP_ACADEMIC_PROGRAM = STPR_ACAD_PROGRAM
                           LEFT JOIN MAJORS AS MAIN_MAJOR ON SAPV.STP_MAJOR1 = MAIN_MAJOR.MAJORS_ID
                           LEFT JOIN MAJORS AS ADDNL_MAJOR
                                     ON STUDENT_MAJORS.STPR_ADDNL_MAJORS = ADDNL_MAJOR.MAJORS_ID
                  WHERE STP_PROGRAM_TITLE IN ('Health Sciences', 'Public Health')
                    AND STP_START_DATE <= GETDATE()
                    AND STP_END_DATE IS NULL
                    AND STP_EVAL_COMBINED_GPA >= 3.5
--(End 1)---------------------------------------------------------------------------------------------------------------
              ) AS X
         GROUP BY STUDENT_ID,
                NAME_LAST,
                NAME_FIRST,
                CLASS_LEVEL_DESC,
                PROGRAM_START_DATE,
                CATALOG_YEAR,
                ANTIC_COMPLETION_DATE,
                EVAL_COMB_CRED,
                  GPA_FOR_ACAD_LEVEL,
                  MAJOR1
--(End 2)-------------------------------------------------------------------------------------------------------------
ORDER BY NAME_FIRST


