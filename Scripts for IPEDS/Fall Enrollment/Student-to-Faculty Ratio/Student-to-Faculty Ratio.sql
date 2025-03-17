SELECT STTR_STUDENT
      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
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
                             AND STP_START_DATE <= '2024-12-12') ranked
                     WHERE rn = 1)

          AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS NOT IN ('Did Not Enroll')
        AND STTR_ACAD_LEVEL = 'GR'
        AND (
            STTR_STUDENT_LOAD IN ('F', 'O')
          )
--Of the full-time students reported in Line F1, the number enrolled in stand-alone graduate or professional programs


SELECT STTR_STUDENT
      FROM STUDENT_TERMS_VIEW
               JOIN PERSON ON STTR_STUDENT = PERSON.ID
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
                             AND STP_START_DATE <= '2024-12-12') ranked
                     WHERE rn = 1)

          AS SAPV ON STUDENT_TERMS_VIEW.STTR_STUDENT = SAPV.STUDENT_ID
      WHERE STUDENT_TERMS_VIEW.STTR_TERM = '2024FA'
        AND SAPV.STP_CURRENT_STATUS NOT IN ('Did Not Enroll')
        AND STTR_ACAD_LEVEL = 'GR'
        AND (
            STTR_STUDENT_LOAD NOT IN ('F', 'O')
            OR STTR_STUDENT_LOAD IS NULL
          )
--Of the part-time students reported in Line F4, the number enrolled in stand-alone graduate or professional programs


SELECT PERSTAT_HRP_ID,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME
        FROM PERSTAT
         JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
         JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        WHERE PERSTAT_END_DATE IS NULL
          AND PERSTAT_START_DATE <= '2024-11-01'
          AND PERSTAT_STATUS = 'FT'
          AND POS_CLASS = 'FAC'
ORDER BY LAST_NAME, FIRST_NAME
--Number of full-time instructional staff (non-medical) as reported on the HR survey component


SELECT *
FROM (
SELECT PERSTAT_HRP_ID,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME,
       CASE WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND CS_NAME LIKE '%-5%') THEN 1 ELSE 0 END AS GRAD_CLASSES,
        CASE WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND CS_NAME NOT LIKE '%-5') THEN 1 ELSE 0 END AS UNDERGRAD_CLASSES
        FROM PERSTAT
         JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
         JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        WHERE PERSTAT_END_DATE IS NULL
          AND PERSTAT_START_DATE <= '2024-11-01'
          AND PERSTAT_STATUS = 'FT'
          AND POS_CLASS = 'FAC') AS X
WHERE GRAD_CLASSES = 1 AND UNDERGRAD_CLASSES = 0
--Of the full-time instructional staff reported in Line F9, the number teaching exclusively in stand-alone graduate or professional programs


SELECT *
FROM (
SELECT PERSTAT_HRP_ID,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME,
       CASE
        WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND FAC_CS_LOAD > 0) THEN 1 ELSE 0 END AS FOR_CREDIT,
        CASE
        WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND (FAC_CS_LOAD IS NULL OR FAC_CS_LOAD = 0)) THEN 1 ELSE 0 END AS NOT_FOR_CREDIT
        FROM PERSTAT
         JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
         JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        WHERE PERSTAT_END_DATE IS NULL
          AND PERSTAT_START_DATE <= '2024-11-01'
          AND PERSTAT_STATUS = 'FT'
          AND POS_CLASS = 'FAC') AS X
WHERE FOR_CREDIT = 0 AND NOT_FOR_CREDIT = 1
--Of the full-time instructional staff reported in Line F9, the number teaching exclusively non-credit courses

SELECT PERSTAT_HRP_ID,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME,
       POS_TITLE
        FROM PERSTAT
         JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
         JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        WHERE PERSTAT_END_DATE IS NULL
          AND PERSTAT_START_DATE <= '2024-11-01'
          AND PERSTAT_STATUS NOT IN ('FT', 'VOL', 'STU')
        AND POS_TYPE != 'TPT'
          AND POS_CLASS = 'FAC'
ORDER BY LAST_NAME, FIRST_NAME
--Number of part-time instructional staff (non-medical) as reported on the HR survey component

SELECT *
FROM (
SELECT PERSTAT_HRP_ID,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME,
       POS_TITLE,
        CASE WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND CS_NAME LIKE '%-5%') THEN 1 ELSE 0 END AS GRAD_CLASSES,
        CASE WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND CS_NAME NOT LIKE '%-5') THEN 1 ELSE 0 END AS UNDERGRAD_CLASSES
        FROM PERSTAT
         JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
         JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        WHERE PERSTAT_END_DATE IS NULL
          AND PERSTAT_START_DATE <= '2024-11-01'
          AND PERSTAT_STATUS NOT IN ('FT', 'VOL', 'STU')
        AND POS_TYPE != 'TPT'
          AND POS_CLASS = 'FAC'
) AS X
WHERE GRAD_CLASSES = 1 AND UNDERGRAD_CLASSES = 0
--Of the part-time instructional staff reported in Line F12, the number teaching exclusively in stand-alone graduate or professional programs


SELECT *
FROM (
SELECT PERSTAT_HRP_ID,
       PERSON.LAST_NAME,
       PERSON.FIRST_NAME,
       CASE
        WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND FAC_CS_LOAD > 0) THEN 1 ELSE 0 END AS FOR_CREDIT,
        CASE
        WHEN
            EXISTS (
                SELECT FACULTY_ID
                FROM FACULTY_SECTIONS_DETAILS_VIEW
                WHERE FACULTY_ID = PERSTAT_HRP_ID
                AND (FAC_CS_LOAD IS NULL OR FAC_CS_LOAD = 0)) THEN 1 ELSE 0 END AS NOT_FOR_CREDIT
        FROM PERSTAT
         JOIN PERSON ON PERSTAT.PERSTAT_HRP_ID = PERSON.ID
         JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
        WHERE PERSTAT_END_DATE IS NULL
          AND PERSTAT_START_DATE <= '2024-11-01'
          AND PERSTAT_STATUS NOT IN ('FT', 'VOL', 'STU')
            AND POS_TYPE != 'TPT'
          AND POS_CLASS = 'FAC') AS X
WHERE FOR_CREDIT = 0 AND NOT_FOR_CREDIT = 1
--Of the part-time instructional staff reported in Line F12, the number teaching exclusively non-credit courses





SELECT DISTINCT FACULTY_ID,
       FAC_LAST_NAME,
       FAC_FIRST_NAME,
       CASE WHEN EXISTS (
           SELECT 1
           FROM PERSTAT
           JOIN POSITION ON PERSTAT.PERSTAT_PRIMARY_POS_ID = POSITION.POSITION_ID
           WHERE PERSTAT_END_DATE IS NULL
           AND PERSTAT_START_DATE <= '2024-11-01'
           AND PERSTAT_STATUS NOT IN  ('VOL', 'STU')
           AND POS_TYPE != 'TPT'
           AND POS_CLASS = 'FAC'
       ) THEN 1 ELSE 0 END AS INSTRUCTORS
FROM FACULTY_SECTIONS_DETAILS_VIEW
WHERE CS_TERM = '2024FA'
AND FAC_CS_LOAD > 0



SELECT *
FROM COURSES
WHERE CRS_NAME LIKE '%-5%'