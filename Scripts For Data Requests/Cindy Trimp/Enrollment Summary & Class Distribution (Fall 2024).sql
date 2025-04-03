SELECT DISTINCT SEV.STUDENT_ID,
                CASE
                    WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                        WHEN PROGRAM = 'Accelerated Nursing' THEN 'Graduate and Special'
                        WHEN PROGRAM = 'Non-Degree Seeking Students' THEN 'Miscellaneous'
                        ELSE 'Undergraduate' END
                    WHEN STUDENT_ACAD_LEVEL = 'GR' THEN 'Graduate and Special'
                    WHEN STUDENT_ACAD_LEVEL = 'CE' THEN 'Miscellaneous'
                    END AS STUDENT_CLASSIFICATION,
                CASE
                    WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                        WHEN PROGRAM = 'Accelerated Nursing' THEN 'Accelerated Nursing'
                        WHEN PROGRAM = 'Non-Degree Seeking Students' THEN 'Non-Degree UG'
                        WHEN FM.TERM = '2024FA' THEN CASE
                            WHEN FIRST_ADMIT.STPR_ADMIT_STATUS = 'FY' THEN 'First-Time Beginning Freshman'
                            ELSE 'Other Freshman' END
                        WHEN FM.TERM = '2023FA' THEN 'Sophomores'
                        WHEN FM.TERM = '2022FA' THEN 'Juniors'
                        WHEN FM.TERM = '2021FA' THEN 'Seniors' END
                    WHEN STUDENT_ACAD_LEVEL = 'GR' THEN 'Master''s Candidates'
                    WHEN STUDENT_ACAD_LEVEL = 'CE' THEN 'Continuing Education'
                    END AS STUDENT_SUB_CLASSIFICATION,
                CASE
                    WHEN STUDENT_LOAD IN ('F', 'O') THEN CASE
                        WHEN STUDENT_GENDER = 'M' THEN 'Full-Time Male'
                        WHEN STUDENT_GENDER = 'F' THEN 'Full-Time Female' END
                    ELSE CASE
                        WHEN STUDENT_GENDER = 'M' THEN 'Part-Time Male'
                        WHEN STUDENT_GENDER = 'F' THEN 'Part-Time Female' END END AS LOAD_GENDER,
--------------------------------------------------------------------------------------------------------------------
                STUDENT_ACAD_LEVEL,
                FM.TERM,
                PROGRAM,
                FIRST_ADMIT.STPR_ADMIT_STATUS,
                STUDENT_LOAD,
                STUDENT_GENDER
--------------------------------------------------------------------------------------------------------------------
FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON SEV.STUDENT_ID = FM.ID
LEFT JOIN (SELECT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
               ) ranked
               WHERE ADMIT_RANK = 1
               ) AS FIRST_ADMIT ON SEV.STUDENT_ID = FIRST_ADMIT.STPR_STUDENT
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_PROGRAM_TITLE AS PROGRAM,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                        ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE PROGRAM_RANK = 1
            ) AS SAPV ON SEV.STUDENT_ID = SAPV.STUDENT_ID
WHERE ENROLL_TERM = '2024FA'
AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
SELECT *
FROM STUDENT_ENROLLMENT_VIEW
-----------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------
--(Begin 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SELECT X.*
FROM (
--(Begin 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
         SELECT CASE
                    WHEN STUDENT_SUB_CLASSIFICATION IN (
                                                        'First-Time Beginning Freshman',
                                                        'Other Freshman',
                                                        'Sophomores',
                                                        'Juniors',
                                                        'Seniors',
                                                        'Total Undergraduates'
                        ) THEN 'Undergraduate'
                    WHEN STUDENT_SUB_CLASSIFICATION IN (
                                                        'Master''s Candidates',
                                                        'Accelerated Nursing',
                                                        'Total Graduates and Special'
                        ) THEN 'Graduate and Special'
                    WHEN STUDENT_SUB_CLASSIFICATION IN (
                                                        'Continuing Education',
                                                        'Post-Baccalaureate',
                                                        'Non-Degree UG',
                                                        'International Exchange',
                                                        'Total Miscellaneous'
                        ) THEN 'Miscellaneous'
                    END AS STUDENT_CLASSIFICATION,
                *
         FROM (
--(Begin 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  SELECT CASE
                             WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1 AND GROUPING(STUDENT_CLASSIFICATION) = 0
                                 THEN CASE
                                          WHEN STUDENT_CLASSIFICATION = 'Undergraduate'
                                              THEN 'Total Undergraduates'
                                          WHEN STUDENT_CLASSIFICATION = 'Graduate and Special'
                                              THEN 'Total Graduates and Special'
                                          WHEN STUDENT_CLASSIFICATION = 'Miscellaneous'
                                              THEN 'Total Miscellaneous' END
                             WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1 AND GROUPING(STUDENT_CLASSIFICATION) = 1 THEN
                                 'Grand Total'
                             ELSE STUDENT_SUB_CLASSIFICATION END AS STUDENT_SUB_CLASSIFICATION,
                         SUM(PART_TIME_MALE)                     AS PART_TIME_MALE,
                         SUM(PART_TIME_FEMALE)                   AS PART_TIME_FEMALE,
                         SUM(PART_TIME_TOTAL)                    AS PART_TIME_TOTAL,
                         SUM(FULL_TIME_MALE)                     AS FULL_TIME_MALE,
                         SUM(FULL_TIME_FEMALE)                   AS FULL_TIME_FEMALE,
                         SUM(FULL_TIME_TOTAL)                    AS FULL_TIME_TOTAL,
                         SUM(MALE_TOTAL)                         AS MALE_TOTAL,
                         SUM(FEMALE_TOTAL)                       AS FEMALE_TOTAL,
                         SUM(TOTAL)                              AS TOTAL
                  FROM (
--(Begin 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                           SELECT STUDENT_CLASSIFICATION,
                                  STUDENT_SUB_CLASSIFICATION,
                                  PART_TIME_MALE,
                                  PART_TIME_FEMALE,
                                  (PART_TIME_MALE + PART_TIME_FEMALE)                                     AS PART_TIME_TOTAL,
                                  FULL_TIME_MALE,
                                  FULL_TIME_FEMALE,
                                  (FULL_TIME_MALE + FULL_TIME_FEMALE)                                     AS FULL_TIME_TOTAL,
                                  (PART_TIME_MALE + FULL_TIME_MALE)                                       AS MALE_TOTAL,
                                  (PART_TIME_FEMALE + FULL_TIME_FEMALE)                                   AS FEMALE_TOTAL,
                                  (PART_TIME_MALE + PART_TIME_FEMALE + FULL_TIME_MALE + FULL_TIME_FEMALE) AS TOTAL
                           FROM (
--(Begin 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                    SELECT STUDENT_CLASSIFICATION,
                                           STUDENT_SUB_CLASSIFICATION,
                                           [Part-Time Male]   AS PART_TIME_MALE,
                                           [Part-Time Female] AS PART_TIME_FEMALE,
                                           [Full-Time Male]   AS FULL_TIME_MALE,
                                           [Full-Time Female] AS FULL_TIME_FEMALE
                                    FROM (
--(Begin 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                             SELECT STUDENT_ID,
                                                    CASE
                                                        WHEN STUDENT_SUB_CLASSIFICATION IN (
                                                                                            'First-Time Beginning Freshman',
                                                                                            'Other Freshman',
                                                                                            'Sophomores',
                                                                                            'Juniors',
                                                                                            'Seniors'
                                                            ) THEN 'Undergraduate'
                                                        WHEN STUDENT_SUB_CLASSIFICATION IN (
                                                                                            'Master''s Candidates',
                                                                                            'Accelerated Nursing'
                                                            ) THEN 'Graduate and Special'
                                                        WHEN STUDENT_SUB_CLASSIFICATION IN (
                                                                                            'Continuing Education',
                                                                                            'Post-Baccalaureate',
                                                                                            'Non-Degree UG',
                                                                                           'International Exchange'
                                                            ) THEN 'Miscellaneous'
                                                        END AS STUDENT_CLASSIFICATION,
                                                    STUDENT_SUB_CLASSIFICATION,
                                                    LOAD_GENDER
                                             FROM (
---(Begin 1)-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                      SELECT DISTINCT SEV.STUDENT_ID,
                                                                      CASE
                                                                          WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                                                                            WHEN STUDENT_CURRENT_TYPE = 'NDFTV'
                                                                              THEN 'International Exchange'
                                                                          WHEN PROGRAM = 'Accelerated Nursing'
                                                                              THEN 'Accelerated Nursing'
                                                                          WHEN PROGRAM = 'Non-Degree Seeking Students'
                                                                              THEN 'Non-Degree UG'
                                                                        WHEN STUDENT_CURRENT_TYPE = 'PB'
                                                                                THEN 'Post-Baccalaureate'

                                                                          WHEN STUDENT_CLASS_LEVEL = 'Freshman'
                                                                              THEN CASE
                                                                                       WHEN FIRST_ADMIT.STPR_ADMIT_STATUS = 'FY'
                                                                                           THEN 'First-Time Beginning Freshman'
                                                                                       ELSE 'Other Freshman' END
                                                                          WHEN STUDENT_CLASS_LEVEL = 'Sophomore'
                                                                              THEN 'Sophomores'
                                                                          WHEN STUDENT_CLASS_LEVEL = 'Junior'
                                                                              THEN 'Juniors'
                                                                          WHEN STUDENT_CLASS_LEVEL = 'Senior'
                                                                              THEN 'Seniors'
                                                                          ELSE 'Non-Degree UG' END
                                                                          WHEN STUDENT_ACAD_LEVEL = 'GR'
                                                                              THEN 'Master''s Candidates'
                                                                          WHEN STUDENT_ACAD_LEVEL = 'CE'
                                                                              THEN 'Continuing Education'
                                                                          END                                          AS STUDENT_SUB_CLASSIFICATION,
                                                                      CASE
                                                                          WHEN STUDENT_LOAD IN ('F', 'O') THEN CASE
                                                                                                                   WHEN STUDENT_GENDER = 'M'
                                                                                                                       THEN 'Full-Time Male'
                                                                                                                   WHEN STUDENT_GENDER = 'F'
                                                                                                                       THEN 'Full-Time Female' END
                                                                          ELSE CASE
                                                                                   WHEN STUDENT_GENDER = 'M'
                                                                                       THEN 'Part-Time Male'
                                                                                   WHEN STUDENT_GENDER = 'F'
                                                                                       THEN 'Part-Time Female' END END AS LOAD_GENDER
                                                      FROM STUDENT_ENROLLMENT_VIEW AS SEV
                                                               JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON SEV.STUDENT_ID = FM.ID
                                                               LEFT JOIN (SELECT STPR_STUDENT, STPR_ADMIT_STATUS
                                                                          FROM (SELECT STPR_STUDENT,
                                                                                       STPR_ADMIT_STATUS,
                                                                                       ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                                                                                           ORDER BY STUDENT_PROGRAMS_ADDDATE) AS ADMIT_RANK
                                                                                FROM STUDENT_PROGRAMS_VIEW
                                                                                WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')) ranked
                                                                          WHERE ADMIT_RANK = 1) AS FIRST_ADMIT
                                                                         ON SEV.STUDENT_ID = FIRST_ADMIT.STPR_STUDENT
                                                               JOIN (SELECT *
                                                                     FROM (SELECT STUDENT_ID,
                                                                                  STP_PROGRAM_TITLE                                                                 AS PROGRAM,
                                                                                  STP_CURRENT_STATUS,
                                                                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                                                                      ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                                                                           FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                           WHERE STP_START_DATE <=
                                                                                 (SELECT TOP 1 TERMS.TERM_END_DATE
                                                                                  FROM TERMS
                                                                                  WHERE TERMS_ID = '2024FA')) ranked
                                                                     WHERE PROGRAM_RANK = 1) AS SAPV
                                                                    ON SEV.STUDENT_ID = SAPV.STUDENT_ID
                                                      WHERE ENROLL_TERM = '2024FA'
                                                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                                                        AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) --Original Data
--(End 1)--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                  ) AS X -- Added Student Classification
--(End 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                         ) AS X PIVOT (COUNT(STUDENT_ID) FOR LOAD_GENDER IN (
                                        [Part-Time Male],
                                        [Part-Time Female],
                                        [Full-Time Male],
                                        [Full-Time Female]
                                        )) AS X --Original Pivot Table
--(End 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                ) AS X --With Column Totals
--(End 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                       ) AS X
                  LEFT JOIN (VALUES
                                 ('First-Time Beginning Freshman', 'Freshman'),
                                 ('Other Freshman', 'Freshman')
                             ) AS FRESHMAN(SUBCATEGORY, CATEGORY) ON X.STUDENT_SUB_CLASSIFICATION = CATEGORY --Not sure what to do with this, yet.
                  GROUP BY GROUPING SETS ((STUDENT_SUB_CLASSIFICATION), (STUDENT_CLASSIFICATION), ())
--(End 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
              ) AS X --Appended on Student Classification Again
--(End 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
     ) AS X
LEFT JOIN (VALUES ('Undergraduate', 1), ('Graduate and Special', 2), ('Miscellaneous', 3)) AS ORDER_1(LABEL, N)
ON X.STUDENT_CLASSIFICATION = ORDER_1.LABEL
LEFT JOIN (VALUES
        ('First-Time Beginning Freshman', 1),
        ('Other Freshman', 2),
        ('Sophomores', 3),
        ('Juniors', 4),
        ('Seniors', 5),
        ('Total Undergraduates', 6),
----------------------------------------
        ('Master''s Candidates', 1),
        ('Accelerated Nursing', 2),
        ('Total Graduates and Special', 3),
----------------------------------------
        ('Continuing Education', 1),
        ('Post-Baccalaureate', 2),
        ('Non-Degree UG', 3),
        ('International Exchange', 4),
        ('Total Miscellaneous', 5)
           ) AS ORDER_2(LABEL, N) ON X.STUDENT_SUB_CLASSIFICATION = ORDER_2.LABEL
ORDER BY CASE WHEN STUDENT_CLASSIFICATION IS NULL THEN 1 ELSE 0 END, ORDER_1.N, ORDER_2.N --Gave it an ordering
--(End 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------

SELECT *
FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN (SELECT *
                                                                     FROM (SELECT STUDENT_ID,
                                                                                  STP_PROGRAM_TITLE                                                                 AS PROGRAM,
                                                                                  STP_CURRENT_STATUS,
                                                                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                                                                      ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                                                                           FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                           WHERE STP_START_DATE <=
                                                                                 (SELECT TOP 1 TERMS.TERM_END_DATE
                                                                                  FROM TERMS
                                                                                  WHERE TERMS_ID = '2024FA')) ranked
                                                                     WHERE PROGRAM_RANK = 1) AS SAPV
                                                                    ON SEV.STUDENT_ID = SAPV.STUDENT_ID
WHERE ENROLL_TERM = '2024FA'
AND SEV.STUDENT_ID = '6165903'


SELECT *
FROM STUDENT_ACAD_PROGRAMS_VIEW
WHERE STUDENT_ID = '6165903'
