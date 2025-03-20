SELECT STTR_STUDENT,
       DEGREE_STATUS,
       CASE
           WHEN DISTANCE = 1 AND NOT_DISTANCE = 0 THEN 'Enrolled exclusively in distance education courses'
           WHEN DISTANCE = 1 AND NOT_DISTANCE = 1 THEN 'Enrolled in at least one but not all distance education courses'
           ELSE 'Not enrolled in any distance education courses' END AS DISTANCE_STATUS
FROM (
SELECT STTR_STUDENT,
        CASE
            WHEN STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'UG'
            THEN CASE
            WHEN STP_PROGRAM_TITLE = 'Non-Degree Seeking Students' THEN 'Non-Degree Seeking'
            ELSE 'Degree Seeking' END
            WHEN STUDENT_TERMS_VIEW.STTR_ACAD_LEVEL = 'GR' THEN 'Graduate Students'
            END AS DEGREE_STATUS,
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM STUDENT_ENROLLMENT_VIEW
                JOIN Z01_RHC_CLASS_SCHEDULE AS CLASSES
                    ON STUDENT_ENROLLMENT_VIEW.SECTION_COURSE_ID = CLASSES.COURSE_SECTIONS_ID
            WHERE ENROLL_TERM = '2024FA'
            AND STUDENT_ENROLLMENT_VIEW.STUDENT_ID = STTR_STUDENT
            AND CSM_INSTR_METHOD IN ('REMOT', 'CYBER')
            ) THEN 1 ELSE 0 END AS DISTANCE,
        CASE
            WHEN EXISTS (
                SELECT 1
                FROM STUDENT_ENROLLMENT_VIEW
                JOIN Z01_RHC_CLASS_SCHEDULE AS CLASSES
                    ON STUDENT_ENROLLMENT_VIEW.SECTION_COURSE_ID = CLASSES.COURSE_SECTIONS_ID
            WHERE ENROLL_TERM = '2024FA'
            AND STUDENT_ENROLLMENT_VIEW.STUDENT_ID = STTR_STUDENT
            AND CSM_INSTR_METHOD NOT IN ('REMOT', 'CYBER')
            ) THEN 1 ELSE 0 END AS NOT_DISTANCE


FROM STUDENT_TERMS_VIEW
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
                                        WHERE TERMS_ID = '2024FA')
                 ) ranked
            WHERE rn = 1)
            AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
AND SAPV.STP_CURRENT_STATUS != 'Did Not Enroll') AS X



SELECT *
FROM STUDENT_ENROLLMENT_VIEW


SELECT *
FROM COURSE_SECTIONS
WHERE SEC_TERM = '2024FA'


SELECT COURSE_SECTIONS_ID, CSM_INSTR_METHOD
FROM Z01_RHC_CLASS_SCHEDULE
WHERE SEC_TERM = '2024FA'
