SELECT DISTINCT SEV.STUDENT_ID,
                FM.TERM,
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
                PROGRAM
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

SELECT *
FROM STUDENT_ACAD_PROGRAMS_VIEW












SELECT *
FROM (
SELECT DISTINCT STUDENT_ID,
                FM.TERM,
                CASE
                    WHEN STUDENT_ACAD_LEVEL = 'UG' THEN 'Undergraduate'
                    WHEN STUDENT_ACAD_LEVEL = 'GR' THEN 'Graduate'
                    WHEN STUDENT_ACAD_LEVEL = 'CE' THEN 'Miscellaneous'
                    END AS STUDENT_CLASSIFICATION,
                CASE
                    WHEN STUDENT_ACAD_LEVEL = 'UG' THEN CASE
                        WHEN FM.TERM = '2024FA' THEN CASE
                            WHEN FIRST_ADMIT.STPR_ADMIT_STATUS = 'FY' THEN 'First-Time Beginning Freshman'
                            ELSE 'Other Freshman' END
                        WHEN FM.TERM = '2023FA' THEN 'Sophomores'
                        WHEN FM.TERM = '2022FA' THEN 'Juniors'
                        WHEN FM.TERM = '2021FA' THEN 'Seniors' END
                    WHEN STUDENT_ACAD_LEVEL = 'GR' THEN 'Graduate'
                    WHEN STUDENT_ACAD_LEVEL = 'CE' THEN 'Miscellaneous'
                    END AS STUDENT_SUB_CLASSIFICATION
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
WHERE ENROLL_TERM = '2024FA'
AND ENROLL_CURRENT_STATUS IN ('Add', 'New')
AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
) AS X
JOIN STUDENT_ENROLLMENT_VIEW ON X.STUDENT_ID = STUDENT_ENROLLMENT_VIEW.STUDENT_ID
WHERE STUDENT_SUB_CLASSIFICATION = 'Graduate'



