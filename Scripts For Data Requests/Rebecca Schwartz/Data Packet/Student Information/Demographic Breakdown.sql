SELECT  STTR_STUDENT,
        LAST_NAME,
        FIRST_NAME,
        GENDER,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE WHEN STTR_STUDENT_LOAD IN ('F', 'O') THEN 'Full-Time' ELSE 'Part-Time' END AS LOAD,
        CASE
            WHEN STTR_ACAD_LEVEL = 'GR' THEN 'Graduate'
            WHEN STTR_ACAD_LEVEL = 'UG' THEN CASE
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking Undergraduate'
            WHEN FM.TERM = '2024FA' OR FM.TERM = '2025SP' THEN CASE
                WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time Undergraduate'
                WHEN STPR_ADMIT_STATUS IN ('TR', 'RE') THEN 'Transfer-in Undergraduate' END
            ELSE 'Continuing/Returning Undergraduate' END END AS STATUS

FROM STUDENT_TERMS_VIEW AS STV
JOIN PERSON ON STV.STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON PERSON.ID = RACE.ID
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STV.STTR_STUDENT = FM.ID
LEFT JOIN (SELECT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STUDENT_PROGRAMS_ADDDATE) AS rn
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
               ) ranked
               WHERE rn = 1) AS FIRST_ADMIT ON STV.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
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
            WHERE rn = 1) AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
WHERE STTR_TERM = '2024FA'



