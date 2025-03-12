SELECT RACE,
       [First-time],
       [Transfer-in],
       [Continuing/Returning],
       [Non-Degree Seeking]
FROM (
SELECT STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND STPR_ADMIT_STATUS = 'FY'
            THEN 'First-time'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND STPR_ADMIT_STATUS = 'TR'
            THEN 'Transfer-in'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM != '2024FA'
            THEN 'Continuing/Returning'
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students'
            THEN 'Non-Degree Seeking'
            END AS STATUS

FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_START_DATE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY STP_START_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= '2024-12-12'
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
AND STUDENT_TERMS_VIEW.STTR_STUDENT_LOAD = 'F'
AND SAPV.STP_CURRENT_STATUS != 'Not Returned'
AND GENDER = 'M'
AND ACPG_CIP LIKE '52%'
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
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND STPR_ADMIT_STATUS = 'FY'
            THEN 'First-time'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND STPR_ADMIT_STATUS = 'TR'
            THEN 'Transfer-in'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM != '2024FA'
            THEN 'Continuing/Returning'
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students'
            THEN 'Non-Degree Seeking'
            END AS STATUS

FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_START_DATE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                            ORDER BY STP_START_DATE DESC) AS rn
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_CURRENT_STATUS != 'Changed Program'
                 AND STP_START_DATE <= '2024-12-12'
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
AND STUDENT_TERMS_VIEW.STTR_STUDENT_LOAD = 'F'
AND SAPV.STP_CURRENT_STATUS != 'Not Returned'
AND GENDER = 'F'
AND ACPG_CIP LIKE '52%'
) AS X
PIVOT (COUNT(STTR_STUDENT)
    FOR STATUS IN ([First-time], [Transfer-in], [Continuing/Returning], [Non-Degree Seeking])) as Y --Women
