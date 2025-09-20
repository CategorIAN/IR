                 SELECT IPEDS_RACE.THEIR_DESC AS RACE,
                 IPEDS_RACE.N,
                 STUDENT_ID             AS ID,
                 STUDENT_GENDER AS GENDER
         FROM (
        SELECT *
        FROM (
            VALUES    ('Non-Resident Alien', 'U.S. Nonresident', 1),
                      ('Hispanic/Latino', 'Hispanic/Latino', 2),
                      ('American Indian', 'American Indian or Alaska Native', 3),
                      ('Asian', 'Asian', 4),
                      ('Black or African American', 'Black or African American', 5),
                      ('Hawaiian/Pacific Islander', 'Native Hawaiian or Other Pacific Islander', 6),
                      ('White', 'White', 7),
                      ('Two or More Races', 'Two or more races', 8),
                      ('Unknown', 'Race and ethnicity unknown', 9)) AS IPEDS_RACE(OUR_DESC, THEIR_DESC, N)
        ) AS IPEDS_RACE
         LEFT JOIN (
                    SELECT STUDENT_ID,
                           STUDENT_GENDER,
                           IPEDS_RACE_ETHNIC_DESC,
                           STP_CURRENT_STATUS,
                           STP_END_DATE,
                           ACPG_CIP,
                           MAJOR,
                           MAJ_CIP,
                           ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY MAJOR) AS MAJOR_RANK
                    FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
                    LEFT JOIN ACAD_PROGRAMS AS AP
                    ON SAPV.STP_ACADEMIC_PROGRAM = AP.ACAD_PROGRAMS_ID
                    LEFT JOIN (
                        SELECT MAJORS_ID AS ID,
                               MAJ_DESC AS MAJOR,
                               MAJ_CIP,
                               'Program Major' AS MAJOR_TYPE,
                               NULL AS STUDENT_PROGRAMS_ID,
                               NULL AS STPR_ADDNL_MAJOR_END_DATE
                        FROM MAJORS
                        UNION
                        SELECT MAJORS_ID AS ID,
                               MAJ_DESC AS MAJOR,
                               MAJ_CIP,
                               'Additional Major',
                               STUDENT_PROGRAMS_ID,
                               STPR_ADDNL_MAJOR_END_DATE
                        FROM STPR_MAJOR_LIST
                        JOIN MAJORS ON STPR_MAJOR_LIST.STPR_ADDNL_MAJORS = MAJORS.MAJORS_ID
                    ) AS ALL_MAJORS
                        ON (
                               MAJOR_TYPE = 'Program Major'
                                AND SAPV.STP_MAJOR1 = ALL_MAJORS.ID
                            )
                        OR (
                                MAJOR_TYPE = 'Additional Major'
                                AND SAPV.STUDENT_ID + '*' + SAPV.STP_ACADEMIC_PROGRAM = ALL_MAJORS.STUDENT_PROGRAMS_ID
                                AND COALESCE(STPR_ADDNL_MAJOR_END_DATE, STP_END_DATE) >= STP_END_DATE
                            )
                    WHERE STP_CURRENT_STATUS = 'Graduated'
                    AND STP_END_DATE BETWEEN '2024-07-01' AND '2025-06-30'
                    AND ACPG_CIP = '11.0701'
                    ) AS STUDENT_PROGRAMS
            ON IPEDS_RACE.OUR_DESC = STUDENT_PROGRAMS.IPEDS_RACE_ETHNIC_DESC
            AND MAJOR_RANK = 2





SELECT SAPV.STUDENT_ID,
       SAPV.STP_PROGRAM_TITLE,
       MAJORS.*
FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
LEFT JOIN ACAD_PROGRAMS AS AP
ON SAPV.STP_ACADEMIC_PROGRAM = AP.ACAD_PROGRAMS_ID
LEFT JOIN (SELECT MAJORS_ID,
                  MAJ_DESC,
                  MAJ_CIP,
                  'Program Major' AS MAJOR_TYPE
           FROM MAJORS AS PROGRAM_MAJOR) AS MAJORS ON SAPV.STP_MAJOR1 = MAJORS.MAJORS_ID


