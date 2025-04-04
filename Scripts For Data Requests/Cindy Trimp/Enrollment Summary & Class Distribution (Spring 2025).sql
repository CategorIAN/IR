--(Begin 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
SELECT X.*
FROM (
--(Begin 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
         SELECT Y.STUDENT_CLASSIFICATION,
                X.*
         FROM (
--(Begin 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                  SELECT CASE
                             WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                AND GROUPING(FRESHMAN) = 1
                                AND GROUPING(STUDENT_CLASSIFICATION) = 0
                                 THEN CASE
                                          WHEN STUDENT_CLASSIFICATION = 'Undergraduate'
                                              THEN 'Total Undergraduates'
                                          WHEN STUDENT_CLASSIFICATION = 'Graduate and Special'
                                              THEN 'Total Graduates and Special'
                                          WHEN STUDENT_CLASSIFICATION = 'Miscellaneous'
                                              THEN 'Total Miscellaneous' END
                            WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                            AND GROUPING(FRESHMAN) = 0
                            AND GROUPING(STUDENT_CLASSIFICATION) = 1
                                THEN CASE
                                    WHEN FRESHMAN = 'Freshman' THEN 'Total Freshman' END
                             WHEN GROUPING(STUDENT_SUB_CLASSIFICATION) = 1
                                AND GROUPING(STUDENT_CLASSIFICATION) = 1
                                 AND GROUPING(FRESHMAN) = 1 THEN 'Grand Total'
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
                                  FRESHMAN,
                                  STUDENT_SUB_CLASSIFICATION,
                                  PART_TIME_MALE,
                                  PART_TIME_FEMALE,
                                  (PART_TIME_MALE + PART_TIME_FEMALE)                                     AS PART_TIME_TOTAL,
                                  FULL_TIME_MALE,
                                  FULL_TIME_FEMALE,
                                  (FULL_TIME_MALE + FULL_TIME_FEMALE)                                     AS FULL_TIME_TOTAL,
                                  (PART_TIME_MALE + FULL_TIME_MALE)                                       AS MALE_TOTAL,
                                  (PART_TIME_FEMALE + FULL_TIME_FEMALE)                                   AS FEMALE_TOTAL,
                                  (PART_TIME_MALE + PART_TIME_FEMALE + FULL_TIME_MALE + FULL_TIME_FEMALE) AS TOTAL,
                                  UNKNOWN
                           FROM (
--(Begin 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                    SELECT STUDENT_CLASSIFICATION,
                                           FRESHMAN,
                                           STUDENT_SUB_CLASSIFICATION,
                                           [Part-Time Male]   AS PART_TIME_MALE,
                                           [Part-Time Female] AS PART_TIME_FEMALE,
                                           [Full-Time Male]   AS FULL_TIME_MALE,
                                           [Full-Time Female] AS FULL_TIME_FEMALE,
                                           [Unknown] AS UNKNOWN
                                    FROM (
--(Begin 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                             SELECT X.STUDENT_ID,
                                                    Y.STUDENT_CLASSIFICATION,
                                                    Z.FRESHMAN,
                                                    X.STUDENT_SUB_CLASSIFICATION,
                                                    X.LOAD_GENDER
                                             FROM (
---(Begin 1)-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                      SELECT DISTINCT SEV.STUDENT_ID,
                                                                      CASE WHEN (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) THEN
                                                                      CASE
                                                                          WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                                                                            WHEN STUDENT_CURRENT_TYPE = 'ACE'
                                                                              THEN 'Early High School'
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
                                                                          END
                                                                          ELSE 'Senior Citizen Auditor' END AS STUDENT_SUB_CLASSIFICATION,
                                                                      CASE
                                                                          WHEN STUDENT_LOAD IN ('F', 'O') THEN CASE
                                                                                                                   WHEN 'M' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                                                       THEN 'Full-Time Male'
                                                                                                                   WHEN 'F' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                                                       THEN 'Full-Time Female'
                                                                                                                    ELSE 'Unknown' END
                                                                          ELSE CASE
                                                                                   WHEN 'M' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                       THEN 'Part-Time Male'
                                                                                   WHEN 'F' IN (STUDENT_GENDER, ASSIGNED_GENDER)
                                                                                       THEN 'Part-Time Female'
                                                                                    ELSE 'Unknown' END END AS LOAD_GENDER
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
                                                               LEFT JOIN (SELECT *
                                                                     FROM (SELECT STUDENT_ID,
                                                                                  STP_PROGRAM_TITLE                                                                 AS PROGRAM,
                                                                                  STP_CURRENT_STATUS,
                                                                                  ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                                                                                      ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                                                                           FROM STUDENT_ACAD_PROGRAMS_VIEW
                                                                           WHERE STP_START_DATE <=
                                                                                 (SELECT TOP 1 TERMS.TERM_END_DATE
                                                                                  FROM TERMS
                                                                                  WHERE TERMS_ID = '2025SP')) ranked
                                                                     WHERE PROGRAM_RANK = 1) AS SAPV
                                                                    ON SEV.STUDENT_ID = SAPV.STUDENT_ID
                                                                LEFT JOIN (VALUES
                                                                                ('6184447', 'F'),
                                                                                ('6184697', 'F'),
                                                                                ('6184977', 'F'),
                                                                                ('6185039', 'F'),
                                                                                ('6186217', 'M'),
                                                                                ('6186670', 'F'),
                                                                                ('6187467', 'F'),
                                                                                ('6187468', 'M'),
                                                                                ('6187470', 'F'),
                                                                                ('6188264', 'F'),
                                                                                ('6188541', 'F'),
                                                                                ('6188544', 'F'),
                                                                                ('6188731', 'F'),
                                                                                ('6188797', 'F'),
                                                                                ('6188940', 'F'),
                                                                                ('6189200', 'M'),
                                                                                ('6189252', 'M'),
                                                                                ('6189523', 'F'),
                                                                                ('6189571', 'F'),
                                                                                ('6189572', 'M'),
                                                                                ('6190155', 'F'),
                                                                                ('6191064', 'F'),
                                                                                ('6191066', 'F'),
                                                                                ('6191067', 'M'),
                                                                                ('6191303', 'M')
                                                                                ) AS Y(ID, ASSIGNED_GENDER)
                                                                                ON SEV.STUDENT_ID = Y.ID
                                                      WHERE ENROLL_TERM = '2025SP'
                                                        AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
                                                        AND ((ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL) OR STUDENT_CURRENT_TYPE = 'SC') --Original Data
--(End 1)--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                  ) AS X
                                    JOIN (VALUES ('First-Time Beginning Freshman', 'Undergraduate'),
                                                 ('Other Freshman', 'Undergraduate'),
                                                 ('Sophomores', 'Undergraduate'),
                                                 ('Juniors', 'Undergraduate'),
                                                 ('Seniors', 'Undergraduate'),
                                                 ('Master''s Candidates', 'Graduate and Special'),
                                                 ('Accelerated Nursing', 'Graduate and Special'),
                                                 ('Continuing Education', 'Miscellaneous'),
                                                 ('Post-Baccalaureate', 'Miscellaneous'),
                                                 ('Early High School', 'Miscellaneous'),
                                                 ('Non-Degree UG', 'Miscellaneous'),
                                                 ('International Exchange', 'Miscellaneous'),
                                                 ('Senior Citizen Auditor', 'Miscellaneous')
                                          ) AS Y(STUDENT_SUB_CLASSIFICATION, STUDENT_CLASSIFICATION)
                                             ON X.STUDENT_SUB_CLASSIFICATION = Y.STUDENT_SUB_CLASSIFICATION
                                    LEFT JOIN (VALUES ('First-Time Beginning Freshman', 'Freshman'),
                                                      ('Other Freshman', 'Freshman')
                                               ) AS Z(STUDENT_SUB_CLASSIFICATION, FRESHMAN)
                                        ON X.STUDENT_SUB_CLASSIFICATION = Z.STUDENT_SUB_CLASSIFICATION
                                             -- Added Student Classification
--(End 2)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                         ) AS X PIVOT (COUNT(STUDENT_ID) FOR LOAD_GENDER IN (
                                        [Part-Time Male],
                                        [Part-Time Female],
                                        [Full-Time Male],
                                        [Full-Time Female],
                                        [Unknown]
                                        )) AS X --Original Pivot Table
--(End 3)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                ) AS X --With Column Totals
--(End 4)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
                       ) AS X
                  GROUP BY GROUPING SETS ((STUDENT_SUB_CLASSIFICATION), (STUDENT_CLASSIFICATION), (FRESHMAN), ())
--(End 5)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
              ) AS X
         JOIN (VALUES ('First-Time Beginning Freshman', 'Undergraduate'),
                       ('Other Freshman', 'Undergraduate'),
                       ('Sophomores', 'Undergraduate'),
                     ('Juniors', 'Undergraduate'),
                     ('Seniors', 'Undergraduate'),
                     ('Master''s Candidates', 'Graduate and Special'),
                     ('Accelerated Nursing', 'Graduate and Special'),
                     ('Continuing Education', 'Miscellaneous'),
                     ('Post-Baccalaureate', 'Miscellaneous'),
                     ('Early High School', 'Miscellaneous'),
                     ('Non-Degree UG', 'Miscellaneous'),
                     ('International Exchange', 'Miscellaneous'),
                     ('Senior Citizen Auditor', 'Miscellaneous'),
             --------------------------------------------------------------------
                    ('Total Freshman', 'Undergraduate'),
                    ('Total Undergraduates', 'Undergraduate'),
                    ('Total Graduates and Special', 'Graduate and Special'),
                    ('Total Miscellaneous', 'Miscellaneous'),
                    ('Grand Total', 'Grand Total')
                                          ) AS Y(STUDENT_SUB_CLASSIFICATION, STUDENT_CLASSIFICATION)
                                             ON X.STUDENT_SUB_CLASSIFICATION = Y.STUDENT_SUB_CLASSIFICATION
         --Appended on Student Classification Again
--(End 6)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
     ) AS X
LEFT JOIN (VALUES ('Undergraduate', 1),
                  ('Graduate and Special', 2),
                  ('Miscellaneous', 3),
                    ('Grand Total', 4))
    AS ORDER_1(LABEL, N)
ON X.STUDENT_CLASSIFICATION = ORDER_1.LABEL
LEFT JOIN (VALUES
        ('First-Time Beginning Freshman', 1),
        ('Other Freshman', 2),
        ('Total Freshman', 3),
        ('Sophomores', 4),
        ('Juniors', 5),
        ('Seniors', 6),
        ('Total Undergraduates', 7),
----------------------------------------
        ('Master''s Candidates', 1),
        ('Accelerated Nursing', 2),
        ('Total Graduates and Special', 3),
----------------------------------------
        ('Continuing Education', 1),
        ('Post-Baccalaureate', 2),
        ('Early High School', 3),
        ('Non-Degree UG', 4),
        ('International Exchange', 5),
        ('Senior Citizen Auditor', 6),
        ('Total Miscellaneous', 7)
           ) AS ORDER_2(LABEL, N) ON X.STUDENT_SUB_CLASSIFICATION = ORDER_2.LABEL
ORDER BY ORDER_1.N, ORDER_2.N --Gave it an ordering
--(End 7)----------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------