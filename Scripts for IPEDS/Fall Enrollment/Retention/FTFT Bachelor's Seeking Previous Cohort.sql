SELECT STV.STTR_STUDENT,
        STP_PROGRAM_TITLE,
       CASE
           WHEN STILL_ENROLLED.STTR_STUDENT IS NULL THEN 0 ELSE 1 END AS STILL_ENROLLED,
        CASE
            WHEN SINCE_GRADUATED.STUDENT_ID IS NULL THEN 0 ELSE 1 END AS SINCE_GRADUATED

FROM STUDENT_TERMS_VIEW AS STV
JOIN PERSON ON STTR_STUDENT = PERSON.ID
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
                                        WHERE TERMS_ID = '2023FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STV.STTR_STUDENT = FM.ID
LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STUDENT_PROGRAMS_ADDDATE) AS rn
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
               ) ranked
               WHERE rn = 1)
    AS FIRST_ADMIT ON STV.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
LEFT JOIN (
    SELECT STTR_STUDENT
    FROM STUDENT_TERMS_VIEW
    WHERE STTR_TERM = '2024FA'
) AS STILL_ENROLLED ON STV.STTR_STUDENT = STILL_ENROLLED.STTR_STUDENT
LEFT JOIN (
    SELECT STUDENT_ID
    FROM STUDENT_ACAD_PROGRAMS_VIEW
    WHERE STP_CURRENT_STATUS_DATE >= (
                     SELECT TOP 1 TERM_START_DATE
                     FROM TERMS
                     WHERE TERMS_ID = '2023FA')
    AND STP_CURRENT_STATUS = 'Graduated'
) AS SINCE_GRADUATED ON STV.STTR_STUDENT = SINCE_GRADUATED.STUDENT_ID
WHERE STV.STTR_TERM = '2023FA'
AND STV.STTR_ACAD_LEVEL = 'UG'
AND STV.STTR_STUDENT_LOAD IN ('F', 'O')
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
AND (STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
AND FM.TERM = '2023FA'
AND STPR_ADMIT_STATUS = 'FY'
)

-----------------------------------------------------------------------------------------------------------------
SELECT *
FROM (
SELECT STV.STTR_STUDENT,
        STP_PROGRAM_TITLE,
       CASE
           WHEN STILL_ENROLLED.STTR_STUDENT IS NULL THEN 0 ELSE 1 END AS STILL_ENROLLED,
        CASE
            WHEN SINCE_GRADUATED.STUDENT_ID IS NULL THEN 0 ELSE 1 END AS SINCE_GRADUATED

FROM STUDENT_TERMS_VIEW AS STV
JOIN PERSON ON STTR_STUDENT = PERSON.ID
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
                                        WHERE TERMS_ID = '2023FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STV.STTR_STUDENT = FM.ID
LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STUDENT_PROGRAMS_ADDDATE) AS rn
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
               ) ranked
               WHERE rn = 1)
    AS FIRST_ADMIT ON STV.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
LEFT JOIN (
    SELECT STTR_STUDENT
    FROM STUDENT_TERMS_VIEW
    WHERE STTR_TERM = '2024FA'
) AS STILL_ENROLLED ON STV.STTR_STUDENT = STILL_ENROLLED.STTR_STUDENT
LEFT JOIN (
    SELECT STUDENT_ID
    FROM STUDENT_ACAD_PROGRAMS_VIEW
    WHERE STP_CURRENT_STATUS_DATE >= (
                     SELECT TOP 1 TERM_START_DATE
                     FROM TERMS
                     WHERE TERMS_ID = '2023FA')
    AND STP_CURRENT_STATUS = 'Graduated'
) AS SINCE_GRADUATED ON STV.STTR_STUDENT = SINCE_GRADUATED.STUDENT_ID
WHERE STV.STTR_TERM = '2023FA'
AND STV.STTR_ACAD_LEVEL = 'UG'
AND STV.STTR_STUDENT_LOAD IN ('F', 'O')
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
AND (STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
AND FM.TERM = '2023FA'
AND STPR_ADMIT_STATUS = 'FY'
)) AS X
WHERE STILL_ENROLLED = 1 OR SINCE_GRADUATED = 1 --Previous Cohort Retained
-----------------------------------------------------------------------------------------------------------------
