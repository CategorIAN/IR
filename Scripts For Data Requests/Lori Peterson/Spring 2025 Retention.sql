SELECT COHORT,
       SUM(STUDENT_COUNT_2025SP) AS STUDENT_COUNT_2025SP
FROM (
SELECT CASE
       WHEN COHORT = '2024FA' THEN 'Freshmen'
        WHEN COHORT = '2023FA' THEN 'Sophomore'
        WHEN COHORT = '2022FA' THEN 'Junior'
        WHEN COHORT = '2021FA' THEN 'Senior'
        WHEN COHORT LIKE '%FA' THEN '5 Year'
        ELSE 'Non-Cohort' END AS COHORT,
    CASE
       WHEN COHORT = '2024FA' THEN 1
        WHEN COHORT = '2023FA' THEN 2
        WHEN COHORT = '2022FA' THEN 3
        WHEN COHORT = '2021FA' THEN 4
        WHEN COHORT LIKE '%FA' THEN 5
        ELSE 6 END AS COHORT_ORDER,
        STUDENT_COUNT_2025SP
FROM (
SELECT COHORT,
       COUNT(STTR_STUDENT) AS STUDENT_COUNT_2025SP
FROM (
SELECT STTR_STUDENT,
       FM.TERM AS COHORT,
       TERM_START_DATE
FROM (
SELECT DISTINCT STTR_STUDENT
FROM STUDENT_TERMS_VIEW AS STV
JOIN (SELECT *
           FROM (SELECT STUDENT_ID,
                        STP_ACADEMIC_PROGRAM,
                        STP_PROGRAM_TITLE,
                        STP_CURRENT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STUDENT_ID
                ORDER BY CASE WHEN STP_END_DATE IS NULL THEN 0 ELSE 1 END, STP_END_DATE DESC) AS PROGRAM_RANK
                 FROM STUDENT_ACAD_PROGRAMS_VIEW
                 WHERE STP_START_DATE <= (SELECT TOP 1 TERMS.TERM_END_DATE
                                        FROM TERMS
                                        WHERE TERMS_ID = '2025SP')
                 ) ranked
            WHERE PROGRAM_RANK = 1
            AND STP_CURRENT_STATUS != 'Did Not Enroll'
            AND STP_PROGRAM_TITLE != 'Non-Degree Seeking Students'
            )
            AS SAPV ON STV.STTR_STUDENT = SAPV.STUDENT_ID
LEFT JOIN (SELECT DISTINCT STPR_STUDENT, STPR_ADMIT_STATUS
           FROM (
               SELECT   STPR_STUDENT,
                        STPR_ADMIT_STATUS,
                        ROW_NUMBER() OVER (PARTITION BY STPR_STUDENT
                        ORDER BY STPR_ADMIT_STATUS) AS ADMIT_RANK
               FROM STUDENT_PROGRAMS_VIEW
               WHERE STPR_ADMIT_STATUS IN ('FY', 'TR', 'RE')
               ) ranked
               WHERE ADMIT_RANK = 1
               AND STPR_ADMIT_STATUS = 'FY'
               )
    AS FIRST_ADMIT ON STV.STTR_STUDENT = FIRST_ADMIT.STPR_STUDENT
JOIN STUDENT_ENROLLMENT_VIEW AS SEV ON STV.STTR_STUDENT = SEV.STUDENT_ID AND STV.STTR_TERM = SEV.ENROLL_TERM
WHERE STV.STTR_TERM = '2025SP'
AND (ENROLL_SCS_PASS_AUDIT != 'A' OR ENROLL_SCS_PASS_AUDIT IS NULL)
AND ENROLL_CURRENT_STATUS IN ('Add', 'New')) AS MY_STUDENTS
JOIN Z01_AAV_STUDENT_FIRST_MATRIC AS FM ON MY_STUDENTS.STTR_STUDENT = FM.ID
JOIN TERMS ON FM.TERM = TERMS.TERMS_ID
) AS X
GROUP BY COHORT, TERM_START_DATE) AS X) AS X
GROUP BY COHORT, COHORT_ORDER
ORDER BY COHORT_ORDER

