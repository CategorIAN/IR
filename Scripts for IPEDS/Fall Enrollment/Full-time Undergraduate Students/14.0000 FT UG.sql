SELECT RACE,
       [First-time],
       [Transfer-in],
       [Continuing/Returning],
       [Non-Degree Seeking]
FROM (
SELECT STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
            WHEN FM.TERM = '2024FA' THEN CASE
                WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time'
                WHEN STPR_ADMIT_STATUS = 'TR' THEN 'Transfer-in' END
            ELSE 'Continuing/Returning' END AS STATUS

FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STPR_ADMIT_STATUS) AS rn
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR')
               ) ranked
               WHERE rn = 1)
    AS FIRST_ADMIT ON STUDENT_TERMS_VIEW.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
JOIN ACAD_PROGRAMS ON SAPV.STP_ACADEMIC_PROGRAM = ACAD_PROGRAMS_ID
WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
AND STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'UG'
AND STUDENT_TERMS_VIEW.STTR_STUDENT_LOAD IN ('F', 'O')
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
AND GENDER = 'M'
AND ACPG_CIP LIKE '14%'
) AS X
PIVOT (COUNT(STTR_STUDENT)
    FOR STATUS IN ([First-time], [Transfer-in], [Continuing/Returning], [Non-Degree Seeking])) as Y --Men


SELECT RACE,
       [First-time],
       [Transfer-in],
       [Continuing/Returning],
       [Non-Degree Seeking]
FROM (
SELECT STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
            WHEN FM.TERM = '2024FA' THEN CASE
                WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time'
                WHEN STPR_ADMIT_STATUS = 'TR' THEN 'Transfer-in' END
            ELSE 'Continuing/Returning' END AS STATUS

FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STPR_ADMIT_STATUS) AS rn
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR')
               ) ranked
               WHERE rn = 1)
    AS FIRST_ADMIT ON STUDENT_TERMS_VIEW.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
JOIN ACAD_PROGRAMS ON SAPV.STP_ACADEMIC_PROGRAM = ACAD_PROGRAMS_ID
WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
AND STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'UG'
AND STUDENT_TERMS_VIEW.STTR_STUDENT_LOAD IN ('F', 'O')
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
AND GENDER = 'F'
AND ACPG_CIP LIKE '14%'
) AS X
PIVOT (COUNT(STTR_STUDENT)
    FOR STATUS IN ([First-time], [Transfer-in], [Continuing/Returning], [Non-Degree Seeking])) as Y --Women