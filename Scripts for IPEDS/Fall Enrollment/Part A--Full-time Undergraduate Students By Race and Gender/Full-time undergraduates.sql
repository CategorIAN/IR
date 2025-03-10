SELECT RACE,
       [First-time],
       [Transfer-in],
       [Continuing/Returning],
       [Non-Degree Seeking]
FROM (
SELECT RACE,
       STATUS,
       COUNT(*) AS COUNT
FROM (
    SELECT STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND (STC_CRED_TYPE = 'INST' OR STC_CRED_TYPE IS NULL)
            THEN 'First-time'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND STC_CRED_TYPE = 'TRCR'
            THEN 'Transfer-in'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM_TERM.TERM_START_DATE < '2024-08-01'
            THEN 'Continuing/Returning'
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students'
            THEN 'Non-Degree Seeking'
            END AS STATUS


FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
LEFT JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
JOIN TERMS AS FM_TERM ON FM.TERM = FM_TERM.TERMS_ID
LEFT JOIN (SELECT *
           FROM (SELECT STC_PERSON_ID,
                        STC_REPORTING_TERM,
                        STC_CRED_TYPE,
                        TERMS.TERM_START_DATE,
                        ROW_NUMBER() OVER (PARTITION BY STC_PERSON_ID ORDER BY TERMS.TERM_START_DATE DESC) AS rn
                 FROM STUDENT_ACAD_CRED
                 JOIN TERMS ON STUDENT_ACAD_CRED.STC_REPORTING_TERM = TERMS.TERMS_ID
                 WHERE TERM_START_DATE < '2024-08-01') ranked
           WHERE rn = 1
           ) AS Q1 ON STUDENT_TERMS_VIEW.STTR_STUDENT = Q1.STC_PERSON_ID
WHERE STTR_TERM = '2024FA'
AND STTR_ACAD_LEVEL = 'UG'
AND STTR_STUDENT_LOAD = 'F'
AND SAPV.STP_CURRENT_STATUS = 'Active'
AND GENDER = 'M'
     ) AS Q2
GROUP BY RACE, STATUS) AS Q3
PIVOT (SUM(COUNT) FOR STATUS IN ([First-time], [Transfer-in], [Continuing/Returning], [Non-Degree Seeking])) as Q4




SELECT RACE,
       [First-time],
       [Transfer-in],
       [Continuing/Returning],
       [Non-Degree Seeking]
FROM (
SELECT RACE,
       STATUS,
       COUNT(*) AS COUNT
FROM (
    SELECT STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE,
        CASE
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND (STC_CRED_TYPE = 'INST' OR STC_CRED_TYPE IS NULL)
            THEN 'First-time'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM.TERM = '2024FA'
                AND STC_CRED_TYPE = 'TRCR'
            THEN 'Transfer-in'
            WHEN STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
                AND FM_TERM.TERM_START_DATE < '2024-08-01'
            THEN 'Continuing/Returning'
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students'
            THEN 'Non-Degree Seeking'
            END AS STATUS


FROM STUDENT_TERMS_VIEW
JOIN PERSON ON STTR_STUDENT = PERSON.ID
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS  AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
LEFT JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
JOIN TERMS AS FM_TERM ON FM.TERM = FM_TERM.TERMS_ID
LEFT JOIN (SELECT *
           FROM (SELECT STC_PERSON_ID,
                        STC_REPORTING_TERM,
                        STC_CRED_TYPE,
                        TERMS.TERM_START_DATE,
                        ROW_NUMBER() OVER (PARTITION BY STC_PERSON_ID ORDER BY TERMS.TERM_START_DATE DESC) AS rn
                 FROM STUDENT_ACAD_CRED
                 JOIN TERMS ON STUDENT_ACAD_CRED.STC_REPORTING_TERM = TERMS.TERMS_ID
                 WHERE TERM_START_DATE < '2024-08-01') ranked
           WHERE rn = 1
           ) AS Q1 ON STUDENT_TERMS_VIEW.STTR_STUDENT = Q1.STC_PERSON_ID
WHERE STTR_TERM = '2024FA'
AND STTR_ACAD_LEVEL = 'UG'
AND STTR_STUDENT_LOAD = 'F'
AND SAPV.STP_CURRENT_STATUS = 'Active'
AND GENDER = 'F'
     ) AS Q2
GROUP BY RACE, STATUS) AS Q3
PIVOT (SUM(COUNT) FOR STATUS IN ([First-time], [Transfer-in], [Continuing/Returning], [Non-Degree Seeking])) as Q4

