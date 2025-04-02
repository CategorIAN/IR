SELECT RACE,
       FORMAT(((STUDENT_COUNT * 1.0) / SUM(STUDENT_COUNT) OVER ()), '0.###') AS STUDENT_PERCENTAGE
FROM (
SELECT RACE,
       COUNT(*) AS STUDENT_COUNT
FROM (
SELECT  STTR_STUDENT,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE

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
WHERE STTR_TERM = '2024FA') AS X
GROUP BY RACE) AS X
----------------------------------------------------------------------------------------------------------------------
SELECT RACE,
       FORMAT(((STUDENT_COUNT * 1.0) / SUM(STUDENT_COUNT) OVER ()), '0.###') AS STUDENT_PERCENTAGE
FROM (
SELECT RACE,
       COUNT(*) AS STUDENT_COUNT
FROM (
SELECT  DISTINCT STUDENT_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE

FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON SEV.STUDENT_ID = RACE.ID
WHERE ENROLL_TERM = '2024FA'
AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
) AS X
GROUP BY RACE) AS X
----------------------------------------------------------------------------------------------------------------------

SELECT RACE,
       FORMAT(SUM(STUDENT_PERCENTAGE), '0.###') AS STUDENT_PERCENTAGE
FROM (
SELECT CASE WHEN RANK <= 5 THEN RACE ELSE 'Other' END AS RACE,
       STUDENT_PERCENTAGE
FROM (
SELECT RACE,
       STUDENT_PERCENTAGE,
       RANK() OVER (ORDER BY STUDENT_PERCENTAGE DESC) AS RANK
FROM (
SELECT RACE,
       (STUDENT_COUNT * 1.0) / SUM(STUDENT_COUNT) OVER () AS STUDENT_PERCENTAGE
FROM (
SELECT RACE,
       COUNT(*) AS STUDENT_COUNT
FROM (
SELECT  DISTINCT STUDENT_ID,
        RACE.IPEDS_RACE_ETHNIC_DESC AS RACE

FROM STUDENT_ENROLLMENT_VIEW AS SEV
JOIN Z01_ALL_RACE_ETHNIC_W_FLAGS AS RACE ON SEV.STUDENT_ID = RACE.ID
WHERE ENROLL_TERM = '2024FA'
AND ENROLL_CURRENT_STATUS IN ('New', 'Add')
AND  (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
) AS X
GROUP BY RACE) AS X) AS X) AS X) AS X
GROUP BY RACE
ORDER BY STUDENT_PERCENTAGE DESC