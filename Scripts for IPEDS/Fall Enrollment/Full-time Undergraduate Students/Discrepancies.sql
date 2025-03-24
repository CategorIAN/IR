SELECT STTR_STUDENT,
        STP_PROGRAM_TITLE,
        FIRST_MATRIC,
        FIRST_REG,
        STPR_ADMIT_STATUS,
        STP_CURRENT_STATUS,
        FIRST_TERM,
        MY_TERM,
        CASE
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
            WHEN MY_TERM = '2024FA' THEN CASE
                WHEN STPR_ADMIT_STATUS = 'FY' THEN 'First-time'
                WHEN STPR_ADMIT_STATUS IN ('TR', 'RE') THEN 'Transfer-in' END
            ELSE 'Continuing/Returning' END AS STATUS
FROM (
SELECT STUDENT_TERMS_VIEW.STTR_STUDENT,
        STP_PROGRAM_TITLE,
        FM.TERM AS FIRST_MATRIC,
        FR.STC_TERM AS FIRST_REG,
        STPR_ADMIT_STATUS,
        STP_CURRENT_STATUS,
        FIRST_TERM.STTR_TERM AS FIRST_TERM,
        ISNULL(FM.TERM, FIRST_TERM.STTR_TERM) AS MY_TERM

FROM STUDENT_TERMS_VIEW
JOIN (
    SELECT DISTINCT STUDENT_ID
    FROM STUDENT_ENROLLMENT_VIEW
    WHERE (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
    AND ENROLL_TERM = '2024FA'
) AS THIS_ENROLLMENT ON STUDENT_TERMS_VIEW.STTR_STUDENT = THIS_ENROLLMENT.STUDENT_ID
LEFT JOIN PERSON ON STUDENT_TERMS_VIEW.STTR_STUDENT = PERSON.ID
LEFT JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON STUDENT_TERMS_VIEW.STTR_STUDENT = RACE.ID
LEFT JOIN (SELECT *
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
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FM.ID
LEFT JOIN Z01_AAV_STUDENT_FIRST_REG AS FR ON STUDENT_TERMS_VIEW.STTR_STUDENT = FR.ID
LEFT JOIN (
SELECT STTR_STUDENT,
       STTR_TERM
FROM (
SELECT STTR_STUDENT,
       STTR_TERM,
       ROW_NUMBER() OVER (PARTITION BY STTR_STUDENT ORDER BY TERM_START_DATE) as rn
FROM STUDENT_TERMS_VIEW
JOIN TERMS ON STUDENT_TERMS_VIEW.STTR_TERM = TERMS.TERMS_ID
WHERE STTR_REG_DATE IS NOT NULL
) AS X WHERE rn = 1) AS FIRST_TERM ON STUDENT_TERMS_VIEW.STTR_STUDENT = FIRST_TERM.STTR_STUDENT
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
    AS FIRST_ADMIT ON STUDENT_TERMS_VIEW.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll'
AND STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'UG'
) AS X


-- Need to Add ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')
-- Should not have added ('6188598', '6189583')
-- Need to Remove ('5830177', '6182144')


SELECT *
FROM STUDENT_ACAD_PROGRAMS_VIEW AS SAPV
JOIN PERSON ON SAPV.STUDENT_ID = PERSON.ID
WHERE STUDENT_ID IN ('5830177', '6182144')

SELECT *
FROM Z01_AAV_STUDENT_FIRST_MATRIC
WHERE Z01_AAV_STUDENT_FIRST_MATRIC.ID IN ('5830177', '6182144')

SELECT *
FROM STUDENT_PROGRAMS_VIEW
WHERE STPR_STUDENT IN ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')

SELECT *
FROM STUDENT_ENROLLMENT_DETAIL_VIEW
WHERE STUDENT_ID IN ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')


SELECT * FROM (
SELECT * FROM (
SELECT FIRST_TERM.STUDENT_ID,
       FIRST_TERM.ENROLL_TERM,
       FM.TERM
FROM (
SELECT STUDENT_ID,
       ENROLL_TERM
FROM (
SELECT STUDENT_ID,
       ENROLL_TERM,
       ROW_NUMBER() OVER (PARTITION BY STUDENT_ID ORDER BY TERM_START_DATE) as rn
FROM STUDENT_ENROLLMENT_VIEW
JOIN TERMS ON STUDENT_ENROLLMENT_VIEW.ENROLL_TERM = TERMS.TERMS_ID
AND ENROLL_SCS_PASS_AUDIT != 'A'
) AS X WHERE rn = 1) AS FIRST_TERM
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON FIRST_TERM.STUDENT_ID = FM.ID
WHERE ENROLL_TERM LIKE '202%') AS X
WHERE ENROLL_TERM != TERM) AS X
JOIN STUDENT_ENROLLMENT_VIEW ON X.STUDENT_ID = STUDENT_ENROLLMENT_VIEW.STUDENT_ID
AND ENROLL_SCS_PASS_AUDIT != 'A'



SELECT * FROM (
SELECT FIRST_TERM.STTR_STUDENT,
       FIRST_TERM.STTR_TERM,
       FM.TERM
FROM (
SELECT STTR_STUDENT,
       STTR_TERM
FROM (
SELECT STTR_STUDENT,
       STTR_TERM,
       ROW_NUMBER() OVER (PARTITION BY STTR_STUDENT ORDER BY TERM_START_DATE) as rn
FROM STUDENT_TERMS_VIEW
JOIN TERMS ON STUDENT_TERMS_VIEW.STTR_TERM = TERMS.TERMS_ID
) AS X WHERE rn = 1) AS FIRST_TERM
LEFT JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON FIRST_TERM.STTR_STUDENT = FM.ID
WHERE STTR_TERM LIKE '202%') AS X
WHERE STTR_TERM != TERM

SELECT *
FROM TERMS

SELECT *
FROM STUDENT_ENROLLMENT_VIEW
WHERE STUDENT_ID = '5450448'

SELECT *
FROM STUDENT_TERMS_VIEW
WHERE STTR_STUDENT = '6188095'

SELECT DISTINCT STUDENT_ID
    FROM STUDENT_ENROLLMENT_VIEW
    WHERE ENROLL_SCS_PASS_AUDIT != 'A'
    AND ENROLL_TERM = '2024FA'


SELECT *
    FROM STUDENT_ENROLLMENT_VIEW
WHERE ENROLL_TERM = '2024FA'
AND STUDENT_ID IN ('6189583', '6188598')


SELECT *
FROM STUDENT_TERMS_VIEW
WHERE STTR_STUDENT IN ('6189583', '6188598')
OR STTR_STUDENT IN ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')

SELECT *
FROM STUDENT_ENROLLMENT_VIEW
WHERE STUDENT_ID IN ('6189583', '6188598')
OR STUDENT_ID IN ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')

SELECT *
FROM UNDERGRADS_ENROLLMENT_DETAIL
WHERE STUDENT_ID IN ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')

SELECT * FROM (SELECT ID, LAST_NAME, FIRST_NAME
               FROM PERSON) AS X
JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON X.ID = SAPV.STUDENT_ID
WHERE ID IN ('6187195', '6188245', '6188168', '6188095', '6188789', '6188822', '6187481')


SELECT * FROM (SELECT ID, LAST_NAME, FIRST_NAME
               FROM PERSON) AS X
JOIN STUDENT_ACAD_PROGRAMS_VIEW AS SAPV ON X.ID = SAPV.STUDENT_ID
WHERE ID IN ('6188598', '6189583')